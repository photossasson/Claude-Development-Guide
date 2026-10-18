"""taskflow-tasks: a small MCP server for the TaskFlow example project.

Runs over stdio. Exposes two tools, one resource and one prompt.
Data lives in tasks.json next to this file (or in the path given by TASKFLOW_DATA).
Requires: pip install "mcp>=2,<3"
"""
import json
import os
import pathlib
import sys
from datetime import date

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

DATA = pathlib.Path(os.environ.get("TASKFLOW_DATA", pathlib.Path(__file__).with_name("tasks.json")))
STATUSES = ("open", "doing", "done")

server = MCPServer(
    name="taskflow-tasks",
    instructions="Task list of the TaskFlow project. Use list_tasks before add_task to avoid duplicates.",
)


def load() -> list[dict]:
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding="utf-8"))


def save(tasks: list[dict]) -> None:
    DATA.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@server.tool(description="List tasks. Optional status filter: open, doing or done.")
def list_tasks(status: str | None = None) -> str:
    tasks = load()
    if status:
        if status not in STATUSES:
            raise ToolError(f"unknown status {status!r}; use one of {', '.join(STATUSES)}")
        tasks = [t for t in tasks if t["status"] == status]
    if not tasks:
        return "no tasks"
    return "\n".join(f"#{t['id']} [{t['status']}] {t['title']}" for t in tasks)


@server.tool(description="Add a new open task and return its id. Writes to the task file.")
def add_task(title: str) -> str:
    title = title.strip()
    if not title:
        raise ToolError("title must not be empty")
    if len(title) > 120:
        raise ToolError("title is longer than 120 characters")
    tasks = load()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": title, "status": "open", "created": date.today().isoformat()})
    save(tasks)
    return f"added task #{new_id}"


@server.resource("tasks://summary", name="summary", description="Count of tasks per status", mime_type="text/plain")
def summary() -> str:
    tasks = load()
    counts = {s: sum(t["status"] == s for t in tasks) for s in STATUSES}
    return " | ".join(f"{s}: {n}" for s, n in counts.items())


@server.prompt(description="Draft a short daily standup from the open and in-progress tasks")
def standup(team: str = "TaskFlow") -> str:
    lines = [f"#{t['id']} [{t['status']}] {t['title']}" for t in load() if t["status"] != "done"]
    return (f"Write a three-line standup for the {team} team in Hebrew.\n"
            "Tasks that are not done:\n" + ("\n".join(lines) or "none"))


if __name__ == "__main__":
    print(f"taskflow-tasks using {DATA}", file=sys.stderr)  # stdout is reserved for the protocol
    server.run()  # stdio by default
