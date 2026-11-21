"""Research service."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.research_repository import (
    ResearchRepository
)
from app.llm.hugging_face_client import HuggingFaceLLMClient
from app.services.research_planner import ResearchPlanner
from uuid import UUID

llm_huggingface_client = HuggingFaceLLMClient()
planner = ResearchPlanner(llm_huggingface_client)
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

    async def execute_research_plan(self , question : str):
        # Generate Research Plan 
        plan = await planner.create_plan(question)
        return plan