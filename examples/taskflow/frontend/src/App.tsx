import { useEffect, useState } from "react";
import { createTask, deleteTask, listTasks, updateStatus } from "./api";
import type { Task, TaskStatus } from "./types";

const NEXT_STATUS: Record<TaskStatus, TaskStatus> = {
  todo: "in_progress",
  in_progress: "done",
  done: "todo",
};

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      setTasks(await listTasks());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  async function onAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    await createTask({ title: title.trim() });
    setTitle("");
    await refresh();
  }

  return (
    <main>
      <h1>TaskFlow</h1>
      {error && <p role="alert">{error}</p>}
      <form onSubmit={onAdd}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task title"
          aria-label="New task title"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <span>{t.title}</span>
            <button onClick={() => updateStatus(t.id, NEXT_STATUS[t.status]).then(refresh)}>
              {t.status}
            </button>
            <button onClick={() => deleteTask(t.id).then(refresh)}>×</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
