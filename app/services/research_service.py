"""Research service."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.research_repository import (
    ResearchRepository
)

class ResearchService:
    # The service is responsible for coordinating the application logic.
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ResearchRepository(db)

    async def create_research(self, request):
        payload = request.model_dump(mode="json")
        print(f"Payload Dump : {payload}")
        job = await self.repository.create(payload)
        """Create a new research job."""
        print(f"Research job created in DB : {job.id} and status: {job.status}")
        return job

    async def get_research(self, research_id):
        """Get a research job by its ID."""
        job = await self.repository.get_by_id(research_id)
        if not job: 
            return None
        return job