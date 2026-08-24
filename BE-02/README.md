## Exploring SQLite by hand

Ran queries directly against `tasks.db` using the sqlite3 CLI:

- `UPDATE tasks SET done = 1;` marked all 4 remaining tasks as done.
- `DELETE FROM tasks WHERE done = 1;` then deleted all of them, bringing the count to 0.
- Immediately called `GET /tasks` on the running API (no restart) — it returned `[]`, confirming the API reads live from the same `tasks.db` file DB Browser/sqlite3 CLI writes to. There's no syncing step; it's one source of truth.
