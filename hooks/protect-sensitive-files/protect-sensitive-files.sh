#!/usr/bin/env bash
# protect-sensitive-files.sh
# PreToolUse hook (matcher: Edit|Write|NotebookEdit): blocks edits to
# sensitive files and directories before they happen.
# Exit 0 = no objection; the normal permission flow still applies.
# Exit 2 = block the tool call; stderr is fed back to Claude as the reason.

set -u

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" \
  | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null)

# No file path in the input: nothing to check.
[ -z "$FILE_PATH" ] && exit 0

deny() {
  echo "protect-sensitive-files: editing '$FILE_PATH' is blocked ($1). Ask the user to change this file manually." >&2
  exit 2
}

BASENAME=$(basename "$FILE_PATH")

# 1. Environment files that hold credentials (.env, .env.local, ...).
case "$BASENAME" in
  .env|.env.*) deny "environment file with credentials" ;;
esac

# 2. Anything under a secrets/ directory.
case "$FILE_PATH" in
  secrets/*|*/secrets/*) deny "secrets directory" ;;
esac

# 3. Existing database migrations are append-only: block edits to files
#    under migrations/. (Creating a NEW migration is usually done with a
#    generator via Bash, which this matcher does not cover.)
case "$FILE_PATH" in
  migrations/*|*/migrations/*) deny "database migrations are append-only; create a new migration instead" ;;
esac

exit 0
