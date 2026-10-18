# TaskFlow

Small full-stack task manager used as the running example of the guide.

## Structure
- `backend/`: Python 3.12, FastAPI, SQLite (stdlib sqlite3, no ORM). Entry: `app/main.py`.
- `frontend/`: React 18 + TypeScript + Vite. Entry: `src/App.tsx`.

## Commands
- Backend tests: `cd backend && pytest -q`
- Backend dev server: `cd backend && uvicorn app.main:app --reload`
- Frontend typecheck: `cd frontend && npm run typecheck`

## Conventions
- Python: type hints everywhere; no ORM; parameterized SQL only.
- TypeScript: strict mode; no `any`.
- Task status values: `todo`, `in_progress`, `done` (single source of truth: backend CHECK constraint + `TaskStatus` type).

## Definition of Done
- Tests pass, typecheck passes, no secrets in code, README updated when behavior changes.
