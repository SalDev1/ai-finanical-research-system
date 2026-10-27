"""Research job routes."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    """Validated requirements used to create a research job."""

    requirements: dict[str, Any] = Field(default_factory=dict)


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_research(request: ResearchRequest) -> dict[str, Any]:
    """Create a research job."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Research job creation is not implemented yet",
    )


@router.get("/{research_id}")
def get_research(research_id: UUID) -> dict[str, Any]:
    """Get research status and progress."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Research status lookup is not implemented for {research_id}",
    )


@router.get("/{research_id}/tasks")
def get_research_tasks(research_id: UUID) -> dict[str, Any]:
    """Inspect task status and failures for a research job."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Task lookup is not implemented for {research_id}",
    )


@router.post("/{research_id}/cancel")
def cancel_research(research_id: UUID) -> dict[str, Any]:
    """Request cancellation of a research job."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Research cancellation is not implemented for {research_id}",
    )
