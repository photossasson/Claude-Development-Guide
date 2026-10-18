# Review checklist

Check every changed hunk against each item. Skip items that cannot apply to
the file type (for example, SQL items for a CSS file).

## Correctness
- Off-by-one errors in loops, slices, and pagination.
- Null / None / undefined dereference on any reachable path.
- Wrong operator or inverted condition (`<` vs `<=`, `and` vs `or`).
- Mutation of shared or default-argument state.
- Async: missing `await`, unhandled promise rejection, race on shared state.

## Error handling
- Errors swallowed silently (empty `except` / `catch`, ignored return codes).
- Error messages that leak internals (paths, SQL, tokens) to end users.
- Resources (files, connections, locks) released on every path, including errors.

## Security
- Input from users or the network used without validation.
- SQL built by string concatenation instead of parameters.
- Secrets, tokens, or credentials in code, logs, or error messages.
- Path traversal: user input joined into filesystem paths.
- New dependencies: are they necessary and from a trusted source?

## API and data contracts
- Changed function signatures: are all callers updated?
- Changed response shapes: are clients and tests updated?
- Database schema or model changes: is there a migration story?
- Backwards compatibility: does any consumer rely on the old behavior?

## Tests
- Changed behavior has a changed or new test.
- Tests assert behavior, not implementation details.
- No test was weakened or deleted to make the suite pass.

## Maintainability
- Dead code introduced or left behind.
- Copy-paste duplication of nontrivial logic.
- Misleading names or comments that no longer match the code.
