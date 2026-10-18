#!/usr/bin/env python3
"""audit_log.py

PostToolUse hook (matcher: "*") that appends one JSON line per tool use to
an audit log at $CLAUDE_PROJECT_DIR/.claude/audit.log (falls back to the
current working directory).

Data minimization: the log records WHO did WHAT and WHEN, never full file
contents or tool responses.
- Bash          -> the command, truncated to 300 characters
- Edit/Write    -> the file path only
- other tools   -> the tool_input key names only

Exit codes: 0 on success. On failure, writes to stderr and exits 1, which
surfaces a non-blocking "hook error" notice without disturbing the session.
"""

import json
import os
import sys
from datetime import datetime, timezone

MAX_COMMAND_CHARS = 300


def summarize(tool_name: str, tool_input: dict):
    if tool_name == "Bash":
        command = str(tool_input.get("command", ""))[:MAX_COMMAND_CHARS]
        return {"command": command}
    if tool_name in ("Edit", "Write", "NotebookEdit", "Read"):
        return {"file_path": tool_input.get("file_path") or tool_input.get("notebook_path")}
    # Default: record only the shape of the input, not its values.
    return {"input_keys": sorted(tool_input.keys())}


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print("audit-log: could not parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_name = data.get("tool_name", "unknown")
    tool_input = data.get("tool_input") or {}

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": data.get("hook_event_name", "PostToolUse"),
        "session_id": data.get("session_id"),
        "cwd": data.get("cwd"),
        "tool_name": tool_name,
        "summary": summarize(tool_name, tool_input),
    }

    log_dir = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."), ".claude")
    log_path = os.path.join(log_dir, "audit.log")

    try:
        os.makedirs(log_dir, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as error:
        print(f"audit-log: failed to write {log_path}: {error}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
