from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Task(BaseModel):
    id: int | None = None
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


app = FastAPI()
task_list = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build Task API", done=False),
    Task(id=3, title="Write tests", done=False),
]


@app.get("/")
async def root():
    """Returns basic info about the API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def get_health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks():
    """Returns the full list of tasks."""
    return task_list


@app.get("/tasks/{id}")
async def get_tasks_by_id(id: int):
    """Returns a single task by id, or 404 if not found."""
    for task in task_list:
        if task.id == id:
            return task

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    """Creates a new task with the given title. 400 if title is missing or empty."""
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    task_id = (
        max(task.id for task in task_list if task.id is not None) + 1
        if task_list
        else 1
    )

    new_task = Task(
        id=task_id,
        title=task.title,
        done=False,
    )

    task_list.append(new_task)

    return new_task


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    """Updates a task's title and/or done status. 404 if not found, 400 if body is empty or invalid."""
    if task_update.title is None and task_update.done is None:
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    if task_update.title is not None and not task_update.title.strip():
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    for task in task_list:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.done is not None:
                task.done = task_update.done

            return task

    return JSONResponse(status_code=404, content={"error": "Unknown id"})


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Deletes a task by id. 404 if not found."""
    for task in task_list:
        if task.id == task_id:
            task_list.remove(task)
            return

    return JSONResponse(status_code=404, content={"error": "Unknown id"})
