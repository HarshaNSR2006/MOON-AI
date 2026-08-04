from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.logger import logger
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    uptime = "unknown"
    start_time = getattr(request.app.state, "start_time", None)
    if start_time:
        uptime_delta = datetime.now(timezone.utc) - start_time
        uptime = f"{int(uptime_delta.total_seconds() // 60)} minutes"
    response = HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        uptime=uptime,
    )
    logger.info("Health check returned healthy status")
    return response
