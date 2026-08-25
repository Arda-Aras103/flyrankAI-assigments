# BE-04: Postgres in Docker

## Running Postgres

```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks \
  -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres
```

## Stage 2: Read from Postgres

Verified GET /tasks and GET /tasks/{id} against Postgres — same SQL, same parameterized queries, no code changes needed.

## Stage 3: Full CRUD on Postgres

Verified POST/PUT/DELETE against Postgres — same RETURNING-based SQL, same parameterized queries, no code changes needed. Full cycle tested: create → mark done → delete, all correct status codes (201, 200, 204, 404).
