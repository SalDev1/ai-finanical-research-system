"""Research repository."""
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ResearchJob
from datetime import datetime, timezone, timedelta

class ResearchRepository: 

    def __init__(self, db : AsyncSession):
        self.db = db 

    async def create(self, payload:dict) -> ResearchJob:
        """Create a new research job."""

        print(f"Payload received in repository: {payload}")
        research_job = ResearchJob(request_payload=payload, status="queued", current_stage= "received", plan_version=1, iteration_count=0, budget_limit=1000.00, budget_used=0.00, deadline_at=datetime.now(timezone.utc) + timedelta(hours=1))
        self.db.add(research_job)
        await self.db.commit()
        await self.db.refresh(research_job)
        return research_job

    async def get_by_id(self, research_id: int) :
        return (
            await self.db.get(ResearchJob, research_id)
        )