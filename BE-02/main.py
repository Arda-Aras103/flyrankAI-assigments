from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Field, Session, SQLModel, create_engine, func, select


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore[assignment]
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        count = session.exec(select(func.count()).select_from(Task)).one()
        if count == 0:
            session.add_all(
                [
                    Task(title="Learn FastAPI"),
                    Task(title="Build Task API"),
                    Task(title="Write Tasks"),
                ]
            )
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Returns basic info about the API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def get_health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks(session: Session = Depends(get_session)):
    """Returns the full list of tasks."""
    tasks = session.exec(text("SELECT * FROM tasks")).mappings().all()  # type :ignpre
    return tasks


@app.get("/tasks/{task_id}")
async def get_tasks_by_id(task_id: int, session: Session = Depends(get_session)):
    """Returns a single task by id, or 404 if not found."""
    task = (
        session.exec(
            text("SELECT * FROM tasks WHERE id= :task_id"), params={"task_id": task_id}
        )
        .mappings()
        .first()  # type :ignore
    )
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task not found"})
    return task


@app.post("/tasks", status_code=201)
async def create_task(task_create: TaskCreate, session: Session = Depends(get_session)):
    """Creates a new task with the given title. 400 if title is missing or empty."""
    if not task_create.title or not task_create.title.strip():
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    new_task = (
        session.exec(
            text(
                "INSERT INTO tasks (title, done) VALUES (:title, :done) RETURNING id,title,done"
            ),
            params={"title": task_create.title, "done": False},
        )
        .mappings()
        .first()
    )  # type :ignore
    session.commit()
    return new_task


@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    """Updates a task's title and/or done status. 404 if not found, 400 if body is empty or invalid."""
    if task_update.title is None and task_update.done is None:
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    if task_update.title is not None and not task_update.title.strip():
        return JSONResponse(status_code=400, content={"error": "Bad Request"})

    task = session.get(Task, task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Unknown id"})

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.done is not None:
        task.done = task_update.done

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Deletes a task by id. 404 if not found."""
    task = session.get(Task, task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Unknown id"})

    session.delete(task)
    session.commit()
    return
