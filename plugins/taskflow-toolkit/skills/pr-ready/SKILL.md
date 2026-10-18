---
name: pr-ready
description: Check whether the current branch is ready for a Pull Request. Verifies that tests pass, lint is clean, the changelog is updated, and no debug leftovers remain. Use before opening a PR or whenever asked if the branch is PR-ready.
---

# PR Readiness Check

Run a full readiness check on the current branch and report a clear
GO / NO-GO verdict. Perform the steps below in order. Never fix issues
during this check; only report them.

## Steps

1. **Branch state**
   - Run `git status --short`. Uncommitted changes are a NO-GO finding.
   - Run `git log --oneline main..HEAD` (fall back to `master..HEAD`).
     Zero commits means there is nothing to open a PR for.

2. **Tests**
   - Backend: if `backend/requirements.txt` or `pyproject.toml` exists,
     run `pytest -q` from the backend directory.
   - Frontend: if `package.json` has a `test` script, run `npm test -- --run`
     (or the project's documented test command).
   - Any failing test is a NO-GO finding. Include the failing test names.

3. **Lint**
   - Python: `ruff check .` if ruff is available.
   - JS/TS: `npx --no-install eslint .` if eslint is installed.
   - Lint errors are NO-GO findings; warnings are listed but do not block.

4. **Changelog**
   - Check whether `CHANGELOG.md` was modified on this branch:
     `git diff --name-only main..HEAD` (fall back to `master..HEAD`).
   - If the branch changes production code but not `CHANGELOG.md`,
     report it as a NO-GO finding and propose a one-line entry.

5. **Debug leftovers**
   - Search the branch diff for `console.log`, `debugger`, `print(`
     in production paths, and `TODO` added by this branch.
   - Report each with file and line. `console.log` and `debugger`
     are NO-GO; `print(` and `TODO` are warnings.

## Report format

Summarize as a table: check, status (PASS / FAIL / WARN), details.
End with one line: `READY FOR PR` or `NOT READY: <n> blocking findings`,
followed by the minimal fix list in priority order.
