from fastapi import FastAPI
from src.db.utils import init_db

init_db()

app = FastAPI(
    title="Graduate Work Core API",
    description="Core API for communication between system components",
    version="0.1.1",
)


@app.get("/")
async def root():
    return {
        "message": "Graduate Work Core API",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }
