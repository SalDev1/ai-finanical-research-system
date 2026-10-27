"""Report routes."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/research", tags=["reports"])


@router.get("/{research_id}/report")
def get_research_report(research_id: UUID) -> dict[str, Any]:
    """Retrieve the published report for a research job."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Published report lookup is not implemented for {research_id}",
    )
