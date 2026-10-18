---
name: code-review
description: Structured review of pending git changes. Finds correctness bugs, security issues, and maintainability problems, ordered by severity, without proposing stylistic rewrites. Use when asked to review a diff, a branch, or changes before a commit or pull request.
argument-hint: "[base-branch]"
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash(git diff *) Bash(git log *) Bash(git status *) Bash(git merge-base *)
---

# Code review

Review the pending changes in this repository against a base branch and report
findings ordered by severity.

## Determine scope

1. Base branch: the first argument (`$0`) if provided, otherwise `main`.
2. Collect the change set:
   - `git status --short` for the working tree state.
   - `git diff <base>...HEAD` for committed work on this branch.
   - `git diff HEAD` for uncommitted work.
3. If both diffs are empty, report "No changes to review" and stop.

## Review procedure

For every changed file:

1. Read the whole file, not only the hunks, whenever a change touches control
   flow, state, error handling, or a public interface.
2. Check the change against every item in [checklist.md](checklist.md).
3. For each modified function, find at least one caller and confirm the
   contract (arguments, return shape, raised errors) still holds.
4. Note tests: does the diff add or update tests for the behavior it changes?

## Report format

Produce a single report with these sections:

### Summary
Two or three sentences: what the change does and your overall assessment.

### Findings
One entry per finding, ordered Critical, High, Medium, Low:

- **[Severity] file:line. Title.** What is wrong, why it matters, and a
  concrete suggested fix. Quote the relevant line.

Severity definitions:
- **Critical**: data loss, security vulnerability, or guaranteed runtime failure.
- **High**: incorrect behavior on realistic inputs, broken contract, missing
  error handling on a likely path.
- **Medium**: edge-case bug, missing test for changed behavior, misleading code.
- **Low**: naming, duplication, or clarity issue worth fixing while here.

### Verdict
One line: "Ready to merge", "Ready after fixing High findings", or
"Needs rework", with the reason.

## Rules

- Report only issues you can tie to a specific file and line.
- Do not propose stylistic rewrites or formatting-only changes.
- Do not edit any files; this is a read-only review.
- If you are not sure a finding is real, say so explicitly and mark it Low.
