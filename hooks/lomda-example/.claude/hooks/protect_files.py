#!/usr/bin/env python3
"""PreToolUse hook: deny edits to secrets, lock files and Git internals.

Reads the hook input (JSON) from stdin. Prints a JSON "deny" decision when the
target path is protected; prints nothing and exits 0 otherwise, so the normal
permission flow continues. Never approves anything.
"""
import json
import sys
from pathlib import PurePosixPath

LOCK_FILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock", "Cargo.lock"}
SECRET_SUFFIXES = (".pem", ".key", ".p12")
ALLOWED_ENV = {".env.example", ".env.sample", ".env.template"}


def reason_for(path: str):
    p = PurePosixPath(path.replace("\\", "/"))
    name = p.name
    if ".git" in p.parts:
        return "files inside .git/ are managed by Git"
    if (name == ".env" or name.startswith(".env.")) and name not in ALLOWED_ENV:
        return "environment files can hold credentials"
    if name.endswith(SECRET_SUFFIXES) or "secrets" in p.parts:
        return "key material and the secrets/ folder are off limits"
    if name in LOCK_FILES:
        return "lock files change only through the package manager"
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"protect_files: unreadable hook input: {exc}", file=sys.stderr)
        return 1  # non-blocking error, visible in the transcript
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    why = reason_for(path) if path else None
    if why:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"protect_files blocked this edit: {why} ({PurePosixPath(path.replace(chr(92), '/')).name}). "
                    "Do not try another tool to change it. Tell the user which change is needed so they can make it."
                ),
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
