"""API router configuration."""

from fastapi import APIRouter
from api.routes import health, reports, research
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(research.router)
api_router.include_router(reports.router)
api_router.include_router(health.router)
