# TaskFlow

Task manager: FastAPI backend in `backend/`, React + TypeScript frontend in `frontend/`, SQLite in development.

## Commands
- Backend tests: `cd backend && pytest -q`
- Frontend tests: `cd frontend && npm test`
- Type check: `cd frontend && npm run typecheck`

Detailed conventions live in `.claude/rules/`. Rules with `paths` load only when Claude works on matching files.
