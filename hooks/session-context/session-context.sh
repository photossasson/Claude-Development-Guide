#!/usr/bin/env bash
# session-context.sh
# SessionStart hook (matcher: startup|resume): injects a repository snapshot
# into Claude's context at the start of every session.
# On SessionStart, anything written to stdout on exit 0 is added as context
# that Claude can see (verified against the hooks reference, 28.07.2026).
# Exit codes: always 0. SessionStart cannot block; failures stay silent.

set -u

# Not a git repository: nothing useful to inject.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

echo "## Repository snapshot (injected by session-context hook)"
echo
echo "Branch: $(git branch --show-current 2>/dev/null || echo unknown)"
echo
echo "### Working tree (git status --short, first 30 lines)"
STATUS=$(git status --short 2>/dev/null | head -30)
if [ -n "$STATUS" ]; then
  echo "$STATUS"
else
  echo "(clean)"
fi
echo
echo "### Last 5 commits"
git log --oneline -5 2>/dev/null || echo "(no commits yet)"
echo

# Open Pull Requests via the GitHub CLI, if available and authenticated.
if command -v gh >/dev/null 2>&1; then
  echo "### Open Pull Requests (gh pr list)"
  PRS=$(gh pr list --state open --limit 5 2>/dev/null)
  if [ -n "$PRS" ]; then
    echo "$PRS"
  else
    echo "(none, or gh is not authenticated)"
  fi
fi

exit 0
