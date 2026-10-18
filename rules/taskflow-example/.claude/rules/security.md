# Security

- Never print, log or commit secrets, tokens or the contents of `.env` files.
- Read configuration through `backend/app/settings.py`; never call `os.environ` directly elsewhere.
- Every SQL query uses bound parameters. Never build SQL with f-strings or string concatenation.

These are instructions, not enforcement. The project also blocks edits to `.env` with a PreToolUse hook.
