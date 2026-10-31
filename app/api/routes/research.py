from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
    ResearchStatusResponse,
)
from app.services.research_service import ResearchService

router = APIRouter(prefix="/v1/research", tags=["Research"])

@router.post("", response_model=ResearchResponse ,status_code=status.HTTP_202_ACCEPTED)
async def create_research(request: ResearchRequest, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Create a research job."""
    service = ResearchService(db)

    job = await service.create_research(request)

    print(f"New Job : {job}")

    return ResearchResponse(
        research_id = job.id,
        status = job.status,
        message = "Research request sucessfully queued."
    )


@router.get("/{research_id}")
def get_research(research_id: UUID, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Get research status and progress."""
    service = ResearchService(db)

    job = service.get_research(research_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Research job not found for {research_id}"
        )

    return ResearchStatusResponse(
        research_id=job.id,
        status=job.status,
        current_stage=job.current_stage,
        created_at=job.created_at,
        updated_at=job.updated_at
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
