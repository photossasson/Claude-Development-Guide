# Diagnosis template

Use exactly these sections, in this order.

## Symptom
What happens and what was expected, one or two sentences.

## Reproduction
The smallest known way to trigger the bug (command, request, or test).
Write "Not reproduced" if you could not trigger it, and why.

## Root cause
The single confirmed cause, with the decisive evidence:
file, line, and the quoted code. If unconfirmed, title this section
"Leading hypothesis" instead and state what evidence is missing.

## Trace
The path from input to failure as a short list of file:line hops,
one line per hop, with a phrase describing what happens at each.

## Proposed fix
The minimal change that removes the root cause: which file, which lines,
what the change does. Note any behavior that the fix intentionally alters.

## Regression test
The test that would fail before the fix and pass after it: file, test name,
and what it asserts.

## Other issues noticed
Bugs or risks found along the way but outside this investigation.
Write "None" if empty.
