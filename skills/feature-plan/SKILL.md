---
name: feature-plan
description: Produce a written implementation plan for a feature before any code is written, including scope, affected files, ordered steps, risks, and a test plan.
argument-hint: "[feature description]"
disable-model-invocation: true
disallowed-tools: Edit Write NotebookEdit
---

# Feature plan

Plan the implementation of a feature. This is a planning-only skill: read the
codebase, then produce a plan. Do not modify any files.

Feature to plan: $ARGUMENTS

If no feature description was provided, ask for one and stop.

## Procedure

1. **Clarify scope.** Restate the feature in one sentence. If the request is
   ambiguous on a point that changes the design (data model, API shape, user
   flow), ask one round of focused questions before planning.
2. **Survey the codebase.** Find the modules the feature touches: entry points,
   data models, existing similar features to imitate, and the test layout.
   Record concrete file paths.
3. **Design the change.** Prefer the smallest design consistent with existing
   patterns in this repository. Reuse existing conventions for naming, error
   handling, and validation; do not introduce new frameworks or layers unless
   the feature is impossible without them.
4. **Write the plan** using the structure in
   [plan-template.md](plan-template.md). Every step must name the files it
   changes and end with a verifiable checkpoint (a command to run or a
   behavior to observe).

## Rules

- Steps must be small enough that each leaves the project working: build
  passing and tests green after every step.
- Include test work inside the steps, not as a final afterthought step.
- List real risks (migrations, breaking API changes, concurrency, performance)
  with a mitigation for each; write "None identified" only after looking.
- State every assumption you made where the request was underspecified.
- End with: "Approve this plan or request changes before implementation."
