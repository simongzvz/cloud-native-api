import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL", "")


def get_connection():
    if not DATABASE_URL:
        return None
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if DATABASE_URL:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        done BOOLEAN NOT NULL DEFAULT FALSE
                    );
                    """
                )
            conn.commit()
    yield


app = FastAPI(title="Cloud-Native Task API", lifespan=lifespan)


class TaskCreate(BaseModel):
    title: str


@app.get("/health")
def health_check():
    return {"status": "ok", "db_configured": bool(DATABASE_URL)}


@app.get("/tasks")
def list_tasks():
    if not DATABASE_URL:
        return []
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
        rows = cur.fetchall()
    return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title must not be empty")
    if not DATABASE_URL:
        return {"id": 1, "title": task.title, "done": False}
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done;",
                (task.title,),
            )
            row = cur.fetchone()
        conn.commit()
    return {"id": row[0], "title": row[1], "done": row[2]}
