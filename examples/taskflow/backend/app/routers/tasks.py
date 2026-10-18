"""CRUD routes for tasks."""
from fastapi import APIRouter, HTTPException

from app.database import get_conn
from app.models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _row_to_task(row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        created_at=row["created_at"],
    )


@router.get("", response_model=list[Task])
def list_tasks() -> list[Task]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    return [_row_to_task(r) for r in rows]


@router.post("", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (payload.title, payload.description),
        )
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return _row_to_task(row)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _row_to_task(row)


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    fields = payload.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    sets = ", ".join(f"{k} = ?" for k in fields)
    with get_conn() as conn:
        cur = conn.execute(
            f"UPDATE tasks SET {sets} WHERE id = ?",
            (*fields.values(), task_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    return _row_to_task(row)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
