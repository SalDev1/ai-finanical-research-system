from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.company_repository import (
    CompanyRepository
)

class CompanyService:
    def __init__(self, db : AsyncSession):
        self.db=db
        self.repository = CompanyRepository(db)

    async def create_company(self, request : dict):
        print(f"Payload Dump : {request}")
        company_record_exists = await self.repository.get_company_by_name(request["name"])

        if company_record_exists:
            print(f"Company record already exists in DB : {company_record_exists.id} and name: {company_record_exists.name}")
            return company_record_exists

        company_record = await self.repository.create_company(request)
        print(f"Company record created in DB : {company_record.id} and name: {company_record.name}")
        return company_record

    async def save_financial_records(self, records : list[dict]):
        # Save financial records to the database.
        records = await self.repository.add_financial_facts(records)
        return records