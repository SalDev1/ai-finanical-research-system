"""Research repository."""
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ResearchJob

class ResearchRepository: 

    def __init__(self, db : AsyncSession):
        self.db = db 

    async def create(self, payload:dict) -> ResearchJob:
        """Create a new research job."""
        research_job = ResearchJob(request_payload=payload, status="queued", current_stage= "received")
        self.db.add(research_job)
        await self.db.commit()
        await self.db.refresh(research_job)
        return research_job

    def get_by_id(self, research_id: int) :
        return (
            self.db.query(ResearchJob)
               .filter(ResearchJob.id == research_id)
               .first()
        )