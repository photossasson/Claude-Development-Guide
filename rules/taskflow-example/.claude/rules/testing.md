---
paths:
  - "backend/tests/**/*.py"
  - "frontend/src/**/*.test.{ts,tsx}"
---

# Testing rules

- One behavior per test; the test name states the behavior.
- No real network, clock or shared state; use the fixtures in `backend/tests/conftest.py`.
- A bug fix starts with a failing regression test.
