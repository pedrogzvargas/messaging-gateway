from contextlib import asynccontextmanager
from fastapi import FastAPI
from .contaniner import Container

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.container = Container()
    print("🚀 App starting...")
    yield
    # shutdown
    print("🛑 App shutting down...")
