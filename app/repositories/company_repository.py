from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Company, FinancialFact

class CompanyRepository:
    def __init__(self, db : AsyncSession):
        self.db = db;

    async def create(self, payload : dict) -> Company:
        """Save a new company to the database."""

        print(f"Company data received in repository: {payload}")
        company = Company(**payload)
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def add_financial_facts(self, records : list[FinancialFact]) -> list[FinancialFact]:
        try:
            # Convert the list of dictionaries to FinancialFact (Accept by SQLAlchemy ORM models) instances
            financial_facts = [
                FinancialFact(**record)
                for record in records
            ]
            self.db.add_all(financial_facts)
            await self.db.commit()
            return financial_facts

        except Exception:
            await self.db.rollback()
            raise