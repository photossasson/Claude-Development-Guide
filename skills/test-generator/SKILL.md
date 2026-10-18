---
name: test-generator
description: Generate focused automated tests for a file, function, or module, following the project's existing test framework and conventions.
when_to_use: Use when asked to add tests, improve coverage, or write a regression test for a specific behavior. Do not use for fixing production code.
argument-hint: "[target-file-or-function] [framework]"
arguments: target framework
allowed-tools: Read Grep Glob
---

# Test generator

Write tests for: $target
Framework: $framework

If `$target` is empty, ask what to test and stop. If `$framework` is empty,
detect the framework from the project (test directories, config files,
dependency manifests) and state which one you detected.

## Procedure

1. **Read the target.** Read the target file completely. Identify every public
   behavior: normal paths, error paths, and boundaries.
2. **Learn the local conventions.** Read one or two existing test files closest
   to the target. Match their style exactly: runner, file naming, directory
   placement, fixture usage, assertion style, import paths.
3. **Plan the cases.** Before writing code, list the test cases as one line
   each: name and the single behavior it verifies. Cover, in priority order:
   - the main success path with realistic data;
   - each documented error or exception path;
   - boundaries: empty, zero, one, maximum, malformed input;
   - any bug fix in recent history of the target (regression tests).
4. **Write the tests** following [conventions.md](conventions.md).
5. **Run the tests** with the project's own test command and iterate until
   they pass. If a test fails because of a real bug in the target, keep the
   failing test, mark it as expected-failure per the framework's mechanism,
   and report the bug; do not change production code.

## Rules

- Test files only: never modify production code.
- One behavior per test; the test name states the behavior.
- Deterministic tests only: no real network, no wall clock, no shared state.
- Do not assert on private internals; assert on observable behavior.
- Report at the end: cases added, cases that found real bugs, coverage gaps
  you saw but did not cover, and why.
