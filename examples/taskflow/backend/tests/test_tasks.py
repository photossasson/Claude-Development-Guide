"""API tests for TaskFlow. Run with: pytest"""
import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Point the app at a temporary database BEFORE importing it.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["TASKFLOW_DB"] = _tmp.name

from app.database import init_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    init_db()
    with TestClient(app) as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_and_get_task(client):
    res = client.post("/tasks", json={"title": "Write docs"})
    assert res.status_code == 201
    task = res.json()
    assert task["title"] == "Write docs"
    assert task["status"] == "todo"

    res2 = client.get(f"/tasks/{task['id']}")
    assert res2.status_code == 200
    assert res2.json()["id"] == task["id"]


def test_update_status(client):
    task = client.post("/tasks", json={"title": "Ship it"}).json()
    res = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert res.status_code == 200
    assert res.json()["status"] == "done"


def test_invalid_status_rejected(client):
    task = client.post("/tasks", json={"title": "X"}).json()
    res = client.patch(f"/tasks/{task['id']}", json={"status": "archived"})
    assert res.status_code == 422


def test_missing_task_404(client):
    assert client.get("/tasks/999999").status_code == 404


def test_delete(client):
    task = client.post("/tasks", json={"title": "Temp"}).json()
    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get(f"/tasks/{task['id']}").status_code == 404
