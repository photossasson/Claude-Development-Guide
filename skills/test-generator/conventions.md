# Test writing conventions

General rules first, then framework specifics. Local project conventions
always win over anything here.

## General

- Arrange, Act, Assert: setup, one action, focused assertions, in that order.
- Name states the behavior: `test_create_task_rejects_empty_title`, not
  `test_create_2`.
- One logical assertion target per test; multiple asserts are fine when they
  check one outcome.
- Build test data with the smallest realistic values; extract repeated setup
  into fixtures or helpers only after the third repetition.
- Never sleep to wait for state; poll or await the condition itself.

## pytest (Python)

- Files `test_<module>.py` next to existing tests; functions `test_<behavior>`.
- Use plain `assert`; use `pytest.raises(SpecificError)` for error paths,
  asserting on the message only when the message is part of the contract.
- Use fixtures for shared setup; prefer function scope. Use
  `tmp_path` for filesystem work and `monkeypatch` for env and attributes.
- Parametrize boundary sweeps with `@pytest.mark.parametrize`.
- Expected failures from known bugs: `@pytest.mark.xfail(reason="...")`,
  with the bug described in the reason.
- For FastAPI apps, use the project's existing `TestClient` fixture and
  assert both status code and response body shape.

## Vitest / Jest (TypeScript, JavaScript)

- Files `<module>.test.ts` mirroring the source layout used by the project.
- `describe` per unit, `it("does X when Y")` per behavior.
- Prefer `toEqual` for structure, `toBe` for identity, `toThrow(SpecificError)`
  for error paths; `await expect(p).rejects.toThrow(...)` for async errors.
- Mock at the module boundary (`vi.mock` / `jest.mock`); never mock the unit
  under test.
- Fake timers (`vi.useFakeTimers`) for time-dependent code; restore in
  `afterEach`.
- For React components, test through user-visible behavior (Testing Library
  queries by role and text), not implementation details or state.
