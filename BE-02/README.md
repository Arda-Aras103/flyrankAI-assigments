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

Exploring SQLite by hand

Ran queries directly against tasks.db using the sqlite3 CLI:

```bash
$ sqlite3 BE-02/tasks.db "SELECT * FROM tasks;"
2|Build Task API|0
3|Write tests|0
4|Test görev|0
5|İkinci görev|0

$ sqlite3 BE-02/tasks.db "SELECT * FROM tasks WHERE done = 1;"
(no rows)

$ sqlite3 BE-02/tasks.db "SELECT COUNT(*) FROM tasks;"
4

$ sqlite3 BE-02/tasks.db "UPDATE tasks SET done = 1;"

$ sqlite3 BE-02/tasks.db "DELETE FROM tasks WHERE done = 1;"

$ sqlite3 BE-02/tasks.db "SELECT COUNT(*) FROM tasks;"
0
```

Immediately called GET /tasks on the running API — no restart needed:

```bash
$ curl http://localhost:8000/tasks
[]
```

This confirmed the API reads live from the same tasks.db file the sqlite3 CLI writes to. There's no syncing step; it's one source of truth.

Ran queries directly against `tasks.db` using the sqlite3 CLI:

- `UPDATE tasks SET done = 1;` marked all 4 remaining tasks as done.
- `DELETE FROM tasks WHERE done = 1;` then deleted all of them, bringing the count to 0.
- Immediately called `GET /tasks` on the running API (no restart) — it returned `[]`, confirming the API reads live from the same `tasks.db` file DB Browser/sqlite3 CLI writes to. There's no syncing step; it's one source of truth.

```

```
