---
name: bug-investigation
description: Systematic root-cause investigation of a reported bug. Produces a written diagnosis with file and line evidence before any fix is attempted.
when_to_use: Use when the user reports a bug, an error message, a stack trace, a failing test, or unexpected behavior, and the root cause is not yet known. Do not use for feature requests or for bugs whose cause is already identified.
argument-hint: "[bug description or error message]"
allowed-tools: Read Grep Glob
---

# Bug investigation

Diagnose the root cause of a bug before changing any code. Investigation and
fixing are separate steps: this skill produces a diagnosis, not a patch.

Bug to investigate: $ARGUMENTS

If no bug description was provided above, use the problem described in the
conversation. If neither exists, ask for the symptom, the expected behavior,
and how to reproduce it, then stop.

## Procedure

1. **Restate the symptom.** One sentence: what happens, what was expected.
2. **Locate the failure surface.** From the error message, stack trace, or
   feature name, find the entry point with Grep and Glob, then read the
   relevant files end to end.
3. **Trace the data flow.** Follow the failing value or request from input to
   the point of failure. Record each file:line hop.
4. **Form hypotheses.** List every plausible cause you found, most likely first.
5. **Verify against the code.** For each hypothesis, find concrete evidence
   for or against it: the exact line, the exact condition, the exact input
   that triggers it. Reproduce with the project's test runner when a failing
   test is available.
6. **Write the diagnosis** using the structure in
   [diagnosis-template.md](diagnosis-template.md).

## Rules

- Do not edit source files during the investigation.
- Separate confirmed facts (with file:line evidence) from hypotheses, and
  label each finding as one or the other.
- One root cause per report. If you find independent additional bugs, list
  them under "Other issues noticed" without investigating them.
- If you cannot confirm a root cause, say so and report the strongest
  hypothesis, the missing evidence, and the next diagnostic step you would run.
- End the report by proposing the minimal fix and which test would prove it,
  but wait for approval before implementing.
