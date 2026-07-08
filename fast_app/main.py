from fastapi import FastAPI
from fast_app.api.v1.app.router import  api_router as app_router
from fast_app.api.v1.shared.router import api_router as shared_router
from fast_app.core.lifespan import lifespan
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="Messaging gateway",
        version="1.0",
        description="App to manage WhatsApp messages",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(app_router, prefix="/api/v1")
    app.include_router(shared_router, prefix="/api/v1")

    return app

app = create_app()
