from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
task_list = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build Task API", "done": False},
    {"id": 3, "title": "Write tests", "done": True},
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
        if task["id"] == id:
            return task

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
