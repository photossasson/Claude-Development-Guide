#!/usr/bin/env bash
# lint-gate.sh
# PostToolUse hook (matcher: Edit|Write): lints the file Claude just edited
# and feeds errors back to Claude.
# Exit 0 = no findings, or no relevant linter installed.
# Exit 2 = lint errors found. On PostToolUse the tool already ran, so exit 2
#          does not undo anything; stderr is shown to Claude as feedback so
#          it can fix the issues in the same turn.

set -u

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0
[ -f "$FILE_PATH" ] || exit 0

report_and_block() {
  # $1 = linter name, $2 = findings text
  {
    echo "lint-gate: $1 reported issues in $FILE_PATH:"
    echo "$2" | head -40
    echo "Fix these lint issues before continuing."
  } >&2
  exit 2
}

case "$FILE_PATH" in
  *.py)
    command -v ruff >/dev/null 2>&1 || exit 0
    OUTPUT=$(ruff check --output-format=concise "$FILE_PATH" 2>&1) \
      || report_and_block "ruff" "$OUTPUT"
    ;;
  *.js|*.jsx|*.ts|*.tsx)
    command -v npx >/dev/null 2>&1 || exit 0
    # Only run if eslint is actually installed in the project.
    npx --no-install eslint --version >/dev/null 2>&1 || exit 0
    OUTPUT=$(npx --no-install eslint --no-color "$FILE_PATH" 2>&1) \
      || report_and_block "eslint" "$OUTPUT"
    ;;
esac

exit 0
