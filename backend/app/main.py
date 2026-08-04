from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.commands import router as commands_router
from app.api.health import router as health_router
from app.api.memory import router as memory_router
from app.api.plugins import router as plugins_router
from app.api.voice import router as voice_router
from app.api.agent import router as agent_router
from app.core.config import settings
from app.core.logger import logger
from app.database.base import Base
from app.database.session import engine
from app.plugins.manager import plugin_manager
from app.websocket.routes import router as websocket_router
from app.api.automation import router as automation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)
    Base.metadata.create_all(bind=engine)
    app.state.start_time = datetime.now(timezone.utc)
    try:
        plugin_manager.discover_and_load()
        logger.info("Loaded %s plugin(s)", len(plugin_manager.list_plugins()))
    except Exception as exc:
        logger.exception("Failed to initialize plugins: %s", exc)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    cors_origins = [
        item.strip() for item in settings.cors_origins.split(",") if item.strip()
    ] if settings.cors_origins else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(chat_router, prefix="/chat", tags=["Chat"])
    app.include_router(commands_router, prefix="/commands", tags=["Commands"])
    app.include_router(memory_router, prefix="/memory", tags=["Memory"])
    app.include_router(plugins_router, prefix="/plugins", tags=["plugins"])
    app.include_router(voice_router, prefix="/voice", tags=["Voice"])
    app.include_router(agent_router, prefix="/agent", tags=["Agent"])
    app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
    app.include_router(automation_router, prefix="/automation", tags=["Automation"])

    return app


app = create_app()
