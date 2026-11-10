from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Company, FinancialFact
from sqlalchemy.dialects.postgresql import insert

class CompanyRepository:
    def __init__(self, db : AsyncSession):
        self.db = db;

    async def create_company(self, payload : dict) -> Company:
        """Save a new company to the database."""

        print(f"Company data received in repository: {payload}")
        company = Company(**payload)
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company 

    async def get_company_by_name(self, name: str) -> Company | None:
        """Retrieve a company by its name."""
        result = await self.db.execute(
            select(Company).where(Company.name == name)
        )
        return result.scalar_one_or_none()

    
    async def add_financial_facts(self, records : list[FinancialFact]) -> list[FinancialFact]:
        try:
            # records --> List of dictionaries by default
            # # Convert the list of dictionaries to FinancialFact (Accept by SQLAlchemy ORM models) instances
            # financial_facts = [
            #     FinancialFact(**record)
            #     for record in records
            # ]
            # # Convert ORM objects into dictionaries for bulk INSERT
            # values = [
            #     {
            #         column.name: getattr(ft, column.name)
            #         for column in FinancialFact.__table__.columns
            #         if column.name != "id"
            #     }
            #     for ft in financial_facts
            # ]

            # if not values:
            #     return []
            stmt = insert(FinancialFact).values(records)
            stmt = stmt.on_conflict_do_nothing(
                constraint="uq_financial_facts_unique_observation"
            )
            # self.db.add_all(financial_facts)
            await self.db.execute(stmt)
            await self.db.commit()
            return records

        except Exception:
            await self.db.rollback()
            raise