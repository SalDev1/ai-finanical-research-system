"""Research service."""
from sqlalchemy.orm import Session

from app.repositories.research_repository import (
    ResearchRepository
)

class ResearchService:
    # The service is responsible for coordinating the application logic.
    def __init__(self, db: Session):
        self.db = db
        self.repository = ResearchRepository(db)

    def create_research(self, request):
        payload = request.model_dump(mode="json")
        job = self.repository.create(payload);
        """Create a new research job."""
        return job

    def get_research(self, research_id):
        """Get a research job by its ID."""
        job = self.repository.get_by_id(research_id)
        if not job: 
            return None
        return job