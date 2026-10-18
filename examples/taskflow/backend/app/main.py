"""TaskFlow API entry point.

Run locally:
    uvicorn app.main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import tasks


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TaskFlow API", version="0.1.0", lifespan=lifespan)
app.include_router(tasks.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
