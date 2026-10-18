---
paths:
  - "frontend/src/**/*.{ts,tsx}"
---

# Frontend component rules

- One component per file; the file name matches the component name (`TaskCard.tsx`).
- Fetch data only through the hooks in `frontend/src/api/`; components never call `fetch` directly.
- Every interactive element has an accessible name (visible label or `aria-label`).
