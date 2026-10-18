"""02_code_reviewer.py

A complete development-task agent built with the Claude Agent SDK (Python).
Companion file for chapter 32 of the guide (מדריך פיתוח ב-Claude Code).

The agent runs eight phases, each one a separate query() call with its own
minimal permission set, all chained to one session through `resume`:

    1. Take a task from the operator (command line).
    2. Research the repository, read-only (Read, Glob, Grep).
    3. Produce a plan as structured output validated against PLAN_SCHEMA.
    4. Human approval gate: print the plan and stop on input().
    5. Execute the change with file edits only (Bash removed from context).
    6. Run tests: only pre-approved `python -m pytest` commands.
    7. Bounded fix loop while tests fail (MAX_FIX_ATTEMPTS), then a
       self-review of `git diff`.
    8. Final structured report plus per-phase cost and turn accounting.

Usage:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=your-api-key
    python 02_code_reviewer.py \\
        --repo ~/projects/taskflow \\
        --task "Add a completed_at timestamp to tasks when they are marked done"

Exit codes:
    0  success, or the operator rejected the plan (no changes were made)
    1  the change was applied but tests still fail after the fix loop
    2  the run stopped early (planning failed, budget exceeded, SDK error)

Logging goes to stderr, human-facing output (plan, report) to stdout, so the
log can be redirected separately: `python 02_code_reviewer.py ... 2>agent.log`.

Run it on a cloned repository or a separate branch: the agent edits real
files, and Git is your safety net.

Verified against:
    https://code.claude.com/docs/en/agent-sdk/python      (checked 29.07.2026)
    https://code.claude.com/docs/en/agent-sdk/permissions
    https://code.claude.com/docs/en/agent-sdk/structured-outputs
    https://code.claude.com/docs/en/agent-sdk/sessions
    Package: claude-agent-sdk 0.2.139. Rebuilt 18.10.2026 from the excerpts
    quoted in chapter 32; py_compile, import and API-name checks against the
    installed package. No end-to-end run against the API in the authoring
    environment (no API key), see qa-findings F-001.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    CLIConnectionError,
    CLIJSONDecodeError,
    PermissionResultDeny,
    ProcessError,
    ResultMessage,
    ToolPermissionContext,
    ToolUseBlock,
    query,
)

# ---------------------------------------------------------------------------
# Part 1: configuration and guardrails (one screen for a security review)
# ---------------------------------------------------------------------------

TOTAL_BUDGET_USD = 3.00      # hard cap for the whole run (client-side estimate)
PHASE_BUDGET_USD = 1.00      # cap for each single query() call
MAX_FIX_ATTEMPTS = 2         # bounded fix loop when tests fail
TRANSIENT_RETRIES = 2        # retries for transport/process failures

GLOBAL_DENY_RULES = [
    "Bash(git push *)",       # an automated agent never pushes to a remote
    "Bash(rm -rf *)",         # no recursive deletes
    "Bash(sudo *)",           # no privilege escalation
    "Read(.env)",             # secrets never enter the context
    "Edit(.env)",
    "WebFetch",               # bare tool name: removes the network tools entirely
    "WebSearch",
]

DANGEROUS_COMMAND_MARKERS = [
    "git push", "rm -rf", "sudo", "curl", "wget", "pip install",
    "npm install", "chmod 777", "> /dev/", "mkfs", "shutdown",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("code-reviewer")

# ---------------------------------------------------------------------------
# Part 2: output schemas (JSON Schema). Optional fields stay optional so the
# model is never pushed to invent content just to satisfy the schema.
# ---------------------------------------------------------------------------

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "task_summary": {"type": "string"},
        "files_to_change": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["path", "reason"],
            },
        },
        "steps": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "test_command": {"type": "string"},
    },
    "required": ["task_summary", "files_to_change", "steps", "test_command"],
}

TEST_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "passed": {"type": "boolean"},
        "summary": {"type": "string"},
        "failing_tests": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["passed", "summary"],
}

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "what_changed": {"type": "string"},
        "changed_files": {"type": "array", "items": {"type": "string"}},
        "tests_passed": {"type": "boolean"},
        "review_notes": {"type": "array", "items": {"type": "string"}},
        "follow_ups": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["what_changed", "changed_files", "tests_passed"],
}

# ---------------------------------------------------------------------------
# Part 3: the permission callback. It is only reached by requests that were
# not already approved by allowed_tools or the permission mode, so the
# default answer is "deny", and every denial is logged.
# ---------------------------------------------------------------------------


async def guard_tool(
    tool_name: str, input_data: dict[str, Any], context: ToolPermissionContext
):
    if tool_name == "Bash":
        command = str(input_data.get("command", ""))
        for marker in DANGEROUS_COMMAND_MARKERS:
            if marker in command:
                log.warning("DENIED dangerous command: %s", command)
                return PermissionResultDeny(
                    message=f"Command contains forbidden pattern '{marker}'. "
                    "This agent may only run the approved test commands.",
                    interrupt=True,  # stop the whole current turn
                )
        log.info("DENIED unapproved command: %s", command)
        return PermissionResultDeny(
            message="Only the pre-approved pytest commands are allowed in this phase."
        )
    log.info("DENIED unapproved tool: %s", tool_name)
    return PermissionResultDeny(
        message=f"Tool {tool_name} is not part of this phase's allowed set."
    )


# ---------------------------------------------------------------------------
# Part 4: run state, phase runner, cost accounting and retry policy
# ---------------------------------------------------------------------------


class BudgetExceeded(RuntimeError):
    """Raised when the accumulated cost crosses TOTAL_BUDGET_USD."""


@dataclass
class RunState:
    session_id: str | None = None
    total_cost_usd: float = 0.0
    turns: int = 0
    log_lines: list[str] = field(default_factory=list)


async def _as_stream(text: str) -> AsyncIterator[dict[str, Any]]:
    """Wrap a prompt as a one-message stream.

    The Python SDK only accepts can_use_tool when the prompt is an
    AsyncIterable (streaming mode), so every phase sends its prompt this way.
    """
    yield {
        "type": "user",
        "message": {"role": "user", "content": text},
        "parent_tool_use_id": None,
    }


async def run_phase(
    state: RunState, phase: str, prompt: str, options: ClaudeAgentOptions
) -> ResultMessage:
    """Run one query() call, log progress, collect the ResultMessage, account cost."""
    log.info("[%s] starting", phase)
    result: ResultMessage | None = None

    for attempt in range(1, TRANSIENT_RETRIES + 2):
        result = None
        try:
            async for message in query(prompt=_as_stream(prompt), options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, ToolUseBlock):
                            log.info("[%s] tool: %s", phase, block.name)
                elif isinstance(message, ResultMessage):
                    result = message
            break
        except (CLIConnectionError, ProcessError, CLIJSONDecodeError) as exc:
            # Transport failure: worth a retry with backoff.
            if result is not None:
                log.warning("[%s] query ended with an error result: %s", phase, exc)
                break
            log.warning("[%s] transient failure (attempt %d): %s", phase, attempt, exc)
            if attempt <= TRANSIENT_RETRIES:
                await asyncio.sleep(2**attempt)
                continue
            raise
        except Exception as exc:
            # A one-shot query() raises a regular exception after an error
            # ResultMessage. If we already have the result, it is a phase
            # outcome, not a crash: return it and let the phase logic decide.
            if result is None:
                raise
            log.warning("[%s] query ended with an error result: %s", phase, exc)
            break

    if result is None:
        raise RuntimeError(f"[{phase}] no result message received")

    # Accounting: keep the shared session, accumulate cost and turns.
    if result.session_id:
        state.session_id = result.session_id
    cost = result.total_cost_usd or 0.0
    state.total_cost_usd += cost
    state.turns += result.num_turns
    line = (
        f"phase={phase} subtype={result.subtype} turns={result.num_turns} "
        f"cost=${cost:.2f} total=${state.total_cost_usd:.2f}"
    )
    state.log_lines.append(line)
    log.info("[%s] done: %s", phase, line)

    if state.total_cost_usd > TOTAL_BUDGET_USD:
        raise BudgetExceeded(
            f"Total budget ${TOTAL_BUDGET_USD:.2f} exceeded "
            f"(~${state.total_cost_usd:.2f}) after phase '{phase}'."
        )
    return result


def structured(result: ResultMessage) -> dict[str, Any] | None:
    """Return the validated structured output, or None if the phase failed."""
    if result.subtype != "success":
        return None
    output = result.structured_output
    return output if isinstance(output, dict) else None


def print_plan(plan: dict[str, Any]) -> None:
    print("\n=== Proposed plan ===")
    print(f"Task: {plan['task_summary']}")
    print("Files to change:")
    for entry in plan["files_to_change"]:
        print(f"  - {entry['path']}: {entry['reason']}")
    print("Steps:")
    for number, step in enumerate(plan["steps"], start=1):
        print(f"  {number}. {step}")
    risks = plan.get("risks") or []
    print("Risks:")
    if risks:
        for risk in risks:
            print(f"  - {risk}")
    else:
        print("  (none reported)")
    print(f"Test command: {plan['test_command']}")


def print_accounting(state: RunState) -> None:
    print("\n=== Run accounting (client-side estimates) ===")
    for line in state.log_lines:
        print(f"  {line}")
    print(f"Total: ~${state.total_cost_usd:.2f}, {state.turns} agentic turns")


# ---------------------------------------------------------------------------
# Part 5: main() with the eight phases
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan, approve, apply and verify one development task with Claude."
    )
    parser.add_argument("--repo", required=True, help="path to the Git repository")
    parser.add_argument("--task", required=True, help="the task, in plain language")
    args = parser.parse_args(argv)
    repo = Path(args.repo).expanduser().resolve()
    if not (repo / ".git").exists():
        parser.error(f"{repo} is not a Git repository (run git init first)")
    args.repo = str(repo)
    return args


async def run(args: argparse.Namespace) -> int:
    state = RunState()

    # Phases 1-3: research, read-only, ending in a structured plan.
    research_options = ClaudeAgentOptions(
        cwd=args.repo,
        system_prompt=(
            "You are a careful senior engineer. Research the repository and plan "
            "the requested change. You are in a READ-ONLY phase: do not modify "
            "anything. The test command in your plan must be runnable from the "
            "repository root and must start with 'python -m pytest'."
        ),
        allowed_tools=["Read", "Glob", "Grep"],
        disallowed_tools=GLOBAL_DENY_RULES,
        permission_mode="dontAsk",  # anything not pre-approved is denied
        max_turns=25,
        max_budget_usd=PHASE_BUDGET_USD,
        output_format={"type": "json_schema", "schema": PLAN_SCHEMA},
    )
    result = await run_phase(
        state,
        "research",
        f"Task: {args.task}\n\n"
        "Explore the repository (start with CLAUDE.md and README.md if present), "
        "find every place the task touches, and return a plan: the files to "
        "change with a reason for each, ordered steps, risks, and the exact "
        "test command.",
        research_options,
    )
    plan = structured(result)
    if plan is None:
        log.error("Planning failed (subtype=%s). No files were touched.", result.subtype)
        print_accounting(state)
        return 2

    # Phase 4: human approval gate. Default is "no"; a rejection is a clean exit.
    print_plan(plan)
    answer = input("\nApprove this plan and apply the change? [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("Plan rejected by operator. No changes were made.")
        return 0

    # Phase 5: execute with file edits only. Bash is removed from the context.
    execute_options = ClaudeAgentOptions(
        cwd=args.repo,
        resume=state.session_id,  # keep the research context
        allowed_tools=["Read", "Edit", "Glob", "Grep"],
        disallowed_tools=GLOBAL_DENY_RULES + ["Bash"],  # bare name: no shell at all
        permission_mode="acceptEdits",
        can_use_tool=guard_tool,
        max_turns=30,
        max_budget_usd=PHASE_BUDGET_USD,
    )
    result = await run_phase(
        state,
        "execute",
        "The operator approved the plan below. Implement it exactly, editing only "
        "the listed files unless a step strictly requires another one. Do not run "
        "any commands.\n\n" + json.dumps(plan, indent=2),
        execute_options,
    )
    if result.subtype != "success":
        log.warning("Execute phase ended with subtype=%s; verifying anyway.", result.subtype)

    # Phases 6-7: tests with a bounded fix loop.
    test_options = ClaudeAgentOptions(
        cwd=args.repo,
        resume=state.session_id,
        allowed_tools=["Read", "Glob", "Grep", "Bash(python -m pytest *)"],
        disallowed_tools=GLOBAL_DENY_RULES,
        permission_mode="dontAsk",
        max_turns=10,
        max_budget_usd=PHASE_BUDGET_USD,
        output_format={"type": "json_schema", "schema": TEST_RESULT_SCHEMA},
    )
    fix_options = ClaudeAgentOptions(
        cwd=args.repo,
        resume=state.session_id,
        allowed_tools=["Read", "Edit", "Glob", "Grep", "Bash(python -m pytest *)"],
        disallowed_tools=GLOBAL_DENY_RULES,
        permission_mode="acceptEdits",
        can_use_tool=guard_tool,
        max_turns=20,
        max_budget_usd=PHASE_BUDGET_USD,
    )

    tests_passed = False
    for attempt in range(MAX_FIX_ATTEMPTS + 1):
        test_options.resume = state.session_id
        result = await run_phase(
            state,
            f"test-{attempt}",
            f"Run the test suite with: {plan['test_command']}\n"
            "Report whether it passed and which tests failed.",
            test_options,
        )
        outcome = structured(result)
        if outcome and outcome.get("passed"):
            tests_passed = True
            break
        if attempt >= MAX_FIX_ATTEMPTS:
            log.error("Tests still failing after %d fix attempts.", MAX_FIX_ATTEMPTS)
            break
        failing = (outcome or {}).get("failing_tests") or ["(test phase did not report names)"]
        fix_options.resume = state.session_id
        await run_phase(
            state,
            f"fix-{attempt + 1}",
            "These tests fail after your change:\n- "
            + "\n- ".join(failing)
            + "\n\nFix only what is needed to make them pass, without changing the "
            "intent of the approved plan and without weakening or deleting tests. "
            f"Verify with: {plan['test_command']}",
            fix_options,
        )

    # Phase 8: self-review of the real diff on disk, then the final report.
    review_options = ClaudeAgentOptions(
        cwd=args.repo,
        resume=state.session_id,
        allowed_tools=["Read", "Glob", "Grep", "Bash(git diff *)", "Bash(git status *)"],
        disallowed_tools=GLOBAL_DENY_RULES,
        permission_mode="dontAsk",
        max_turns=10,
        max_budget_usd=PHASE_BUDGET_USD,
        output_format={"type": "json_schema", "schema": REPORT_SCHEMA},
    )
    result = await run_phase(
        state,
        "review",
        "Review your own change. Run 'git status --short' and 'git diff --stat', "
        "then read the full 'git diff' for each changed file. Report what actually "
        "changed on disk, list edge cases that are not covered by a test as "
        "review_notes, and suggest follow-ups. "
        f"The final test run {'passed' if tests_passed else 'FAILED'}; "
        "set tests_passed accordingly.",
        review_options,
    )
    report = structured(result) or {
        "what_changed": "(review phase failed; inspect git diff manually)",
        "changed_files": [],
        "tests_passed": tests_passed,
    }
    report["tests_passed"] = tests_passed  # the test phase is the source of truth

    print("\n=== Final report ===")
    print(f"What changed: {report['what_changed']}")
    print(f"Changed files: {', '.join(report['changed_files']) or '(none reported)'}")
    print(f"Tests passed: {report['tests_passed']}")
    for note in report.get("review_notes") or []:
        print(f"Review note: {note}")
    for item in report.get("follow_ups") or []:
        print(f"Follow-up: {item}")
    print_accounting(state)

    return 0 if tests_passed else 1


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return asyncio.run(run(args))
    except BudgetExceeded as exc:
        log.error("%s", exc)
        return 2
    except KeyboardInterrupt:
        log.error("Interrupted by operator.")
        return 2
    except Exception as exc:  # noqa: BLE001 - report any SDK failure with a clear exit code
        log.error("Run failed: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
