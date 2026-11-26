"""Evidence repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Source

class SourceRepository:
    def __init__(self, db : AsyncSession):
        self.db = db 

    async def save_source(self, payload : dict) -> Source:
        "Save a new evidence record in the db"
        evidence_payload = Source(**payload)
        self.db.add(evidence_payload)
        await self.db.commit()
        await self.db.refresh(evidence_payload)
        return evidence_payload

    async def get_source_record(self, evidence_id : str) -> Source | None:
        "Get evidence record using it's ID" 
        source_record = await self.db.execute(
            select(Source).where(Source.id == evidence_id)
        )
        return source_record