"""01_quickstart.py

Minimal Claude Agent SDK example (Python), matching the official quickstart
and chapter 31 of the guide (מדריך פיתוח ב-Claude Code).

What it does:
    Asks the agent to review utils.py in the current directory for bugs that
    would cause crashes and fix them. Read/Edit/Glob are auto-approved and
    file edits are auto-accepted (permission_mode="acceptEdits").

Prerequisites:
    pip install -r requirements.txt          # claude-agent-sdk (pinned)
    export ANTHROPIC_API_KEY=...             # or a claude.ai login via `claude`
    Create a utils.py next to this file with one or two functions that crash
    on empty or None input (as in the official quickstart), then run:
    python 01_quickstart.py

Verified against:
    https://code.claude.com/docs/en/agent-sdk/python  (checked 29.07.2026)
    Package: claude-agent-sdk 0.2.139 (py_compile + import; no API execution
    inside the authoring sandbox, see qa-findings F-001).
"""

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

PROMPT = "Review utils.py for bugs that would cause crashes. Fix any issues you find."


async def main() -> None:
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Glob"],  # auto-approve these tools
        permission_mode="acceptEdits",  # auto-accept file edits
        max_turns=10,  # hard stop for the agentic loop
    )

    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)  # Claude's explanation
                elif isinstance(block, ToolUseBlock):
                    print(f"Tool: {block.name}")  # a tool call
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # "success" or an error subtype
            cost = getattr(message, "total_cost_usd", None)
            if cost is not None:
                print(f"Cost: ${cost:.4f} | turns: {message.num_turns}")


if __name__ == "__main__":
    asyncio.run(main())
