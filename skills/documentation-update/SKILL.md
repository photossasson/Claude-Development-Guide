---
name: documentation-update
description: Bring documentation in line with recent code changes. Updates README, docstrings, API docs, configuration samples, and changelog entries to match what the code actually does.
when_to_use: Use after implementing or merging changes that alter behavior, APIs, configuration, setup steps, or CLI usage. Also use when asked to check whether the docs are stale.
argument-hint: "[optional scope, e.g. 'backend only']"
---

# Documentation update

Update the project's documentation to match its code. Ground every edit in the
actual current behavior of the code, never in what the docs used to say.

Requested scope: $ARGUMENTS

## Recent changes (injected at load time)

Uncommitted changes:
!`git diff HEAD --stat`

Last commits:
!`git log --oneline -10`

## Procedure

1. **Map the change set.** From the file list and commits above, read the full
   diffs that touch behavior, APIs, configuration, or setup. Ignore pure
   refactors that change nothing observable.
2. **Find the affected doc surfaces.** For each behavioral change, check every
   surface listed in [doc-map.md](doc-map.md) that could describe it.
3. **Verify before editing.** For each doc statement you are about to change,
   confirm the new truth by reading the code, not by guessing. For documented
   commands, check that the command as written matches the project's actual
   scripts and entry points.
4. **Edit.** Update stale statements, add missing documentation for new
   behavior, and delete documentation for removed behavior. Match the
   surrounding style, language, heading structure, and formatting.
5. **Report.** List each doc file changed with a one-line reason, plus any
   stale documentation you found that is outside the requested scope.

## Rules

- Never document behavior you have not confirmed in the code.
- Never invent features, flags, or options; if the code is ambiguous, say so
  in the report instead of guessing in the docs.
- Keep examples runnable: exact paths, exact commands, working snippets.
- Do not rewrite sections that are still accurate; smallest diff that makes
  the docs true.
- Docstrings follow the file's existing docstring style; do not introduce a
  new style into a file.
