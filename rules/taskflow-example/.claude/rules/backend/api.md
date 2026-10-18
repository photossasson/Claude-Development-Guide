---
paths:
  - "backend/app/api/**/*.py"
---

# Backend API rules

- Each router lives in `backend/app/api/<resource>.py` and is registered in `backend/app/main.py`.
- Validate every request body with a Pydantic model from `backend/app/schemas/`.
- Return errors as `{"error": {"code": "...", "message": "..."}}` with the matching HTTP status.
- Every new endpoint gets a test in `backend/tests/api/` in the same change.
