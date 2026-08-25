import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, func, select

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_engine(db_url, echo=True)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore[assignment]
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


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
