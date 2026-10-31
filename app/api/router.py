"""API router configuration."""

from fastapi import APIRouter
from app.api.routes import health, reports, research
api_router = APIRouter(prefix="/api")

api_router.include_router(research.router)
api_router.include_router(reports.router)
api_router.include_router(health.router)
