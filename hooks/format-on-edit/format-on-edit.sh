#!/usr/bin/env bash
# format-on-edit.sh
# PostToolUse hook (matcher: Edit|Write): formats the file Claude just edited.
# Python files -> black, web/doc files -> prettier.
# Exit codes: always 0. A formatting failure must never disturb the session,
# so every formatter invocation is best-effort.

set -u

INPUT=$(cat)

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# No file path in the hook input: nothing to format.
[ -z "$FILE_PATH" ] && exit 0

# Only format regular files that still exist.
[ -f "$FILE_PATH" ] || exit 0

case "$FILE_PATH" in
  *.py)
    if command -v black >/dev/null 2>&1; then
      black --quiet "$FILE_PATH" 2>/dev/null || true
    fi
    ;;
  *.js|*.jsx|*.ts|*.tsx|*.json|*.css|*.scss|*.md|*.html|*.yaml|*.yml)
    if command -v npx >/dev/null 2>&1; then
      # --no-install: use the project's prettier only, never download one.
      npx --no-install prettier --write "$FILE_PATH" >/dev/null 2>&1 || true
    fi
    ;;
esac

exit 0
