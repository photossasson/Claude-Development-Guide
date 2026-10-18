#!/usr/bin/env python3
"""PostToolUse hook: run the Hebrew style checker on every edited text file.

When the checker finds problems, the findings go to stderr and the hook exits 2.
For PostToolUse, Claude Code shows that stderr to Claude, which then fixes the
file. The edit itself already happened; this hook gives feedback, it does not undo.
"""
import json
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".html", ".htm", ".txt"}
CHECKER = Path(__file__).with_name("check_style.py")
MAX_LINES = 20


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"hebrew_style_gate: unreadable hook input: {exc}", file=sys.stderr)
        return 1
    path = (data.get("tool_input") or {}).get("file_path") or ""
    target = Path(path)
    if target.suffix.lower() not in TEXT_SUFFIXES or not target.is_file():
        return 0
    if not CHECKER.is_file():
        print(f"hebrew_style_gate: checker not found at {CHECKER}", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, str(CHECKER), str(target)],
                            capture_output=True, text=True, timeout=25)
    if result.returncode == 0:
        return 0
    if result.returncode == 1:
        lines = result.stdout.strip().splitlines()
        shown = "\n".join(lines[:MAX_LINES])
        more = f"\n... and {len(lines) - MAX_LINES} more" if len(lines) > MAX_LINES else ""
        print(f"Hebrew style check failed for {target.name}:\n{shown}{more}\n"
              "Fix every finding in that file without changing code spans, code blocks or URLs.",
              file=sys.stderr)
        return 2
    print(f"hebrew_style_gate: checker error: {result.stderr.strip()[:300]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
