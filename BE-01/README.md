# Task API

A simple CRUD API built with FastAPI.

## Endpoints

| Method | Path          | Description       |
| ------ | ------------- | ----------------- |
| GET    | `/`           | API info          |
| GET    | `/health`     | Health check      |
| GET    | `/tasks`      | List all tasks    |
| GET    | `/tasks/{id}` | Get a single task |
| POST   | `/tasks`      | Create a new task |
| PUT    | `/tasks/{id}` | Update a task     |
| DELETE | `/tasks/{id}` | Delete a task     |

## Running

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Swagger UI

![Swagger UI](./CRUD-swaggerUI.png)
