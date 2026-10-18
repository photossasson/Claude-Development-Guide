# TaskFlow: פרויקט הדוגמה של המדריך

אפליקציית ניהול משימות קטנה: React + TypeScript בצד הלקוח, Python + FastAPI בצד השרת, SQLite לאחסון.

המדריך משתמש בפרויקט הזה כדי להדגים עבודה עם Claude Code לאורך הפרקים: קריאת Codebase (פרק 6), שינוי מבוקר (פרק 9), Debugging (פרק 10), Testing (פרק 11), Refactoring (פרק 12), Git (פרק 13), פיתוח Feature מלא (פרק 34) ו-Capstone (פרק 43).

## הרצה

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Tests:

```bash
cd backend && pytest -q
cd frontend && npm run typecheck
```
