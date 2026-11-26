from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.source_repository import (
    SourceRepository
)
from app.db.models import Source

class SourceRegistry: 
    def __init__(self, db : AsyncSession):
        self.db=db
        self.repository = SourceRepository(db)

    async def source_registry(self, payload : dict) -> Source:
        source_exists = await self.repository.get_source_record(payload.id)
        if source_exists : 
            return source_exists
        new_source_record = await self.repository.save_source(payload)
        return new_source_record
        