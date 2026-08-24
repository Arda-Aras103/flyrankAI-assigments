## Database

This project uses **SQLite** because it needs zero setup (no server to install or configure), stores everything in a single file, and survives restarts without any extra infrastructure — ideal for a small task API.

The database file `tasks.db` is created automatically on first run, in the project root. It is git-ignored, so every fresh clone starts with a clean database that gets seeded automatically.

### Running the project

```bash
cd BE-02
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

On first run, `tasks.db` is created and seeded with three example tasks automatically. No manual setup required.

### Exploring SQLite by hand

Ran queries directly against `tasks.db` using the sqlite3 CLI:

- `UPDATE tasks SET done = 1;` marked all 4 remaining tasks as done.
- `DELETE FROM tasks WHERE done = 1;` then deleted all of them, bringing the count to 0.
- Immediately called `GET /tasks` on the running API (no restart) — it returned `[]`, confirming the API reads live from the same `tasks.db` file DB Browser/sqlite3 CLI writes to. There's no syncing step; it's one source of truth.
