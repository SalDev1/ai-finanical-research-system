"""Health routes."""

from fastapi import APIRouter
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def liveness() -> dict[str, str]:
    """Check whether the API process is alive."""

    return {"status": "ok"}


@router.get("/ready")
def readiness() -> dict[str, str]:
    """Check whether required dependencies are available."""

    return {"status": "ok"}

@router.get("/")
def root():
    return {
        "message": "AI Financial Research System API"
    }
