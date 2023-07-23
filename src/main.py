from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.api.microwaves import router as states_router
from src.backend.api.startup import router as startup_router
from src.backend.api.websockets import router as websocket_router
from src.backend.config import get_settings
from src.frontend.ui import router as ui_router


def app() -> FastAPI:
    """Creates main FastAPI application."""

    settings = get_settings()

    api_app = FastAPI(
        debug=settings.DEBUG,
        title=settings.API_NAME,
        version=settings.API_VERSION,
    )

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["*"],
    )
    api_app.include_router(ui_router)
    api_app.include_router(startup_router)
    api_app.include_router(states_router)
    api_app.include_router(websocket_router)

    return api_app
