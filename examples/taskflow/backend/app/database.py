"""SQLite storage layer for TaskFlow (standard library only, no ORM).

The database path can be overridden with the TASKFLOW_DB environment
variable, which the tests use to point at a temporary file.
"""
import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator

DEFAULT_DB_PATH = os.environ.get("TASKFLOW_DB", "taskflow.db")


def get_db_path() -> str:
    return os.environ.get("TASKFLOW_DB", DEFAULT_DB_PATH)


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'todo'
                    CHECK (status IN ('todo', 'in_progress', 'done')),
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
