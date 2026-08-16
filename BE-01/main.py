from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Task(BaseModel):
    id: int | None = None
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str | None = None


app = FastAPI()
task_list = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build Task API", done=False),
    Task(id=3, title="Write tests", done=False),
]


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def get_health():
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks():
    return task_list


@app.get("/tasks/{id}")
async def get_tasks_by_id(id: int):
    for task in task_list:
        if task.id == id:
            return task

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
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
