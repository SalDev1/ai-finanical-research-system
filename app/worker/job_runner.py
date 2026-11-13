"""Background job runner."""
import time
from datetime import datetime

from sqlalchemy import select, or_, func, text

from app.analysis.financial_analysis import FinancialAnalysis
from app.db.models import ResearchJob
from app.db.session import AsyncSessionLocal, get_db
from app.ingestion.clients.sec_client import SECClient
from app.ingestion.extractors.financial_extractor import FinancialExtractor
from app.services.company_service import CompanyService

# Implementating PostgresDB Backend Job Queue --> Using Postgres SKIP LOCKED Concept which
# helps in achieving atomicity and concurrency control when multiple workers are trying to claim jobs from the queue.

# Func Objective : The worker gets the job ID, commits the claim and can then execute the job outside the transaction.
async def claim_next_job(db, worker_id: str):
    async with AsyncSessionLocal() as db:
        async with db.begin():

            statement = (
                select(ResearchJob)
                .where(
                    ResearchJob.attempt_count
                    < ResearchJob.max_attempts,

                    or_(
                        ResearchJob.status == "queued",
                        (
                            (ResearchJob.status == "running")
                            & (ResearchJob.lease_expires_at < func.now())
                        )
                    )
                )
                .order_by(ResearchJob.created_at)
                .with_for_update(skip_locked=True)
                .limit(1)
            )

            result = await db.execute(statement)
            job = result.scalar_one_or_none()

            if not job:
                return None

            job.status = "running"
            job.current_stage = "executing"
            job.worker_id = worker_id
            job.attempt_count += 1
            # This keeps the lease timestamp based on the PostgresSQL server clock
            job.lease_expires_at = await db.scalar(
                text("SELECT NOW() + INTERVAL '60 seconds'")
            )

            await db.flush()
            return job.id

# Background worker job that process the research jobs stored in the PostgresDB. The worker will claim a job, execute it, and update the job status accordingly.
async def process_job(research_id):
    try:
        job = None
        async with AsyncSessionLocal() as db:
            # All the below lines of code are executed within single DB Async session .
            job = await db.get(ResearchJob, research_id)
            sec = SECClient()
            extractor = FinancialExtractor()
            company_service = CompanyService(db)
            analyzer = FinancialAnalysis()

            if not job or job.status != 'running':
                return 
            
            print(f"Processing job {research_id}...")
            #  Simulate research execution
            user_question = job.request_payload.get("question");
            print(f"Executing research for {user_question}...")

            company_name = None;
            
            if "apple" in user_question.lower():
                company_name = "apple"

            # Fetch company facts from SEC API and extract financial data using the FinancialExtractor.
            company_facts_results = await sec.get_company_facts(company_name)
            job.status = "company_facts_fetched"
            job.current_stage = "company_facts_fetched"
            print(f"Fetched facts for {company_name}")
           
            extract_facts_results = extractor.extract(company_facts_results["company_facts"])
            print(f"Extracted facts for {company_name}: {extract_facts_results['revenue']}")

            normalized_financial_facts = extractor.normailze_finanical_facts(extract_facts_results, company_facts_results);
            job.status = "data_validation_completed"
            job.current_stage = "data_validation_completed"

            print(f"Normalized financial facts for {company_name}: {len(normalized_financial_facts)}")

            company_record = await company_service.create_company({"name": company_name, "ticker": company_facts_results["company_ticker"], "cik": company_facts_results["company_cik"], "created_at": datetime.now()})

            # Attaching company_id to each financial record before storing them in the database as foreign key reference.
            for record in normalized_financial_facts : 
                record["company_id"] = company_record.id

            print(f"Saving {len(normalized_financial_facts)} financial records for company {company_name} to the database.")

            print(f"Record type: {type(normalized_financial_facts)}")
            print(f"First record type: {type(normalized_financial_facts[0]) if normalized_financial_facts else None}")
            db_financial_records = await company_service.save_financial_records(normalized_financial_facts)

            job.status = "data_ingestion_completed"
            job.current_stage = "data_ingestion_completed"

            time.sleep(5)

            # # Analyse financial data using the FinancialAnalysis class.
            analyzer.analyze(normalized_financial_facts)

            job.status = "completed"
            job.current_stage = "completed"
            job.worker_id = None
            job.lease_expires_at = None

            await db.commit()
            print(f"Job {research_id} completed successfully.")

    except Exception:
        await db.rollback()
        raise 

    finally:
       await db.close()
