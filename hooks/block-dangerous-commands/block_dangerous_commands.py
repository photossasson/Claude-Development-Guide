#!/usr/bin/env python3
"""block_dangerous_commands.py

PreToolUse hook (matcher: Bash) that denies destructive shell commands
before they run:

1. Recursive force delete of the root or home directory (rm -rf / ...).
2. Force push to main or master (git push --force / -f / +refspec).
3. Piping a remote download straight into a shell (curl ... | bash).

Safe by design: the script only READS the hook input from stdin and prints
a JSON permission decision to stdout. It never executes the inspected
command and has no side effects.

Output semantics (verified against the hooks reference, 28.07.2026):
- exit 0 with no stdout        -> no objection; normal permission flow.
- exit 0 with permissionDecision "deny" JSON -> the tool call is denied
  and permissionDecisionReason is fed back to Claude.
"""

import json
import re
import sys

# Targets whose recursive force deletion is never acceptable from an agent.
DANGEROUS_RM_TARGETS = {
    "/", "/*", "~", "~/", "~/*",
    "$HOME", "$HOME/", "$HOME/*", "${HOME}", "${HOME}/",
    "/etc", "/usr", "/var", "/home", "/boot", "/bin", "/sbin", "/lib",
}

PROTECTED_BRANCHES = {"main", "master"}

# curl/wget output piped into any shell interpreter.
PIPE_TO_SHELL = re.compile(
    r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(env\s+\S+\s+)?(ba|z|da|k)?sh\b"
)


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def split_segments(command: str):
    """Split a compound command on ;, &&, || and | into simple segments."""
    return [s.strip() for s in re.split(r"\|\||&&|;|\|", command) if s.strip()]


def strip_quotes(token: str) -> str:
    return token.strip("\"'")


def is_dangerous_rm(segment: str) -> bool:
    tokens = segment.split()
    if tokens and tokens[0] == "sudo":
        tokens = tokens[1:]
    if not tokens or tokens[0] != "rm":
        return False
    flag_text = "".join(t for t in tokens[1:] if t.startswith("-") and not t.startswith("--"))
    recursive = "r" in flag_text or "R" in flag_text or "--recursive" in tokens
    force = "f" in flag_text or "--force" in tokens
    if not (recursive and force):
        return False
    targets = [strip_quotes(t) for t in tokens[1:] if not t.startswith("-")]
    return any(t in DANGEROUS_RM_TARGETS for t in targets)


def is_force_push_to_protected(segment: str) -> bool:
    tokens = segment.split()
    if tokens and tokens[0] == "sudo":
        tokens = tokens[1:]
    if len(tokens) < 2 or tokens[0] != "git" or tokens[1] != "push":
        return False
    rest = tokens[2:]
    force = any(t in ("--force", "-f") or t.startswith("--force=") for t in rest)
    refs = [t for t in rest if not t.startswith("-") or t.startswith("+")]
    plus_force = False
    to_protected = False
    for ref in refs:
        name = strip_quotes(ref)
        if name.startswith("+"):
            plus_force = True
            name = name.lstrip("+")
        # Handle refspecs like "local:main" and plain branch names.
        dest = name.split(":")[-1]
        if dest in PROTECTED_BRANCHES or dest in {
            "refs/heads/main", "refs/heads/master"
        }:
            to_protected = True
    return to_protected and (force or plus_force)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Unparseable input: report a non-blocking error so it is visible
        # in the transcript, but do not block the tool call.
        print("block-dangerous-commands: could not parse hook input", file=sys.stderr)
        sys.exit(1)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        sys.exit(0)

    if PIPE_TO_SHELL.search(command):
        deny(
            "Piping a remote download directly into a shell (curl|bash style) "
            "is blocked by policy. Download to a file, review it, then run it "
            "explicitly if the user approves."
        )

    for segment in split_segments(command):
        if is_dangerous_rm(segment):
            deny(
                "Recursive force deletion of the root or home directory is "
                "blocked by policy. Delete specific project paths instead."
            )
        if is_force_push_to_protected(segment):
            deny(
                "Force-pushing to main/master is blocked by policy. Push to a "
                "feature branch and open a Pull Request instead."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
