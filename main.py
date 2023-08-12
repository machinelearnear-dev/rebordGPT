#  import ASSETS_PATH from config file

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from config import ASSETS_PATH
from fastapi.staticfiles import StaticFiles

from search import Search

services = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Load models...")
    services["search"] = Search()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/api/ping")
async def hello():
    return {"message": "pong"}

@app.get("/api/test")
async def test(query: str = None):
    return {"response": query}

@app.get("/api/search")
async def search(query: str = None):
    search = services["search"]
    # validate search has been loaded
    if search is None:
        raise HTTPException(status_code=500, detail="Search module not found")
    response = search.search(query)
    return {"response": response}


app.mount("/", StaticFiles(directory=ASSETS_PATH, html=True), name="static")