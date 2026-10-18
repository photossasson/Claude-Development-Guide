# Implementation plan template

Use exactly these sections, in this order.

## Feature
One-sentence statement of the feature and who it serves.

## Scope
- In scope: bullet list of what will be built.
- Out of scope: bullet list of near-misses deliberately excluded.

## Current state
Short survey of the relevant code as it exists today: key files, the pattern
this feature should imitate, and anything that constrains the design.

## Design decisions
Each decision as one bullet: the choice, the alternative rejected, and why.

## Steps
Numbered, smallest-safe-change order. Each step:

N. **Title.**
   - Files: paths created or changed.
   - Change: what is done.
   - Checkpoint: command to run or behavior to observe that proves the step.

## Test plan
- Unit tests: which behaviors, which files.
- Integration or API tests: which flows.
- Manual check: the one end-to-end scenario to verify by hand.

## Risks and mitigations
One bullet per risk: the risk, its impact, the mitigation.

## Assumptions
Every assumption made where the request was underspecified.

## Estimate
Rough size per step (S / M / L) and overall.
