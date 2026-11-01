"""Background job runner."""
import time
from datetime import timedelta

from sqlalchemy import select, or_, func, text

from app.db.models import ResearchJob
from app.db.session import AsyncSessionLocal, get_db
from app.ingestion.clients.sec_client import SECClient
from app.ingestion.extractors.financial_extractor import FinancialExtractor

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
           
            print(f"Fetched facts for {company_name}")
           
            extract_facts_results = extractor.extract(company_facts_results)
           
            print(f"Extracted facts for {company_name}: {extract_facts_results['operating_cash_flow']}")

            time.sleep(5)

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
