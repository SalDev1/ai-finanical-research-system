"""Research repository."""
from sqlalchemy.orm import Session
from app.db.models import ResearchJob

class ResearchRepository: 

    def __init__(self, db : Session):
        self.db = db 

    def create(self, payload:dict) -> ResearchJob:
        """Create a new research job."""
        research_job = ResearchJob(request_payload=payload, status="queued", current_stage= "received")
        self.db.add(research_job)
        self.db.commit()
        self.db.refresh(research_job)
        return research_job

    def get_by_id(self, research_id: int) :
        return (
            self.db.query(ResearchJob)
               .filter(ResearchJob.id == research_id)
               .first()
        )