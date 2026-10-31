"""Background job runner."""
import time
from datetime import timedelta

from sqlalchemy import select, or_, func, text

from app.db.models import ResearchJob
from app.db.session import get_db

# Implementating PostgresDB Backend Job Queue --> Using Postgres SKIP LOCKED Concept which
# helps in achieving atomicity and concurrency control when multiple workers are trying to claim jobs from the queue.

# Func Objective : The worker gets the job ID, commits the claim and can then execute the job outside the transaction.
def claim_next_job(db, worker_id: str):

    with db.begin():

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

        job = db.execute(statement).scalar_one_or_none()

        if not job:
            return None

        job.status = "running"
        job.current_stage = "executing"
        job.worker_id = worker_id
        job.attempt_count += 1
        # This keeps the lease timestamp based on the PostgresSQL server clock
        job.lease_expires_at = db.scalar(
            text("SELECT NOW() + INTERVAL '60 seconds'")
        )

        db.flush()
        return job.id

# Background worker job that process the research jobs stored in the PostgresDB. The worker will claim a job, execute it, and update the job status accordingly.
def process_job(research_id):

    db = get_db().__next__()

    try:
        job = db.get(ResearchJob, research_id)

        if not job or job.status != 'running':
            return 

        print(f"Processing job {research_id}...")
        #  Simulate research execution
        time.sleep(5)

        job.status = "completed"
        job.current_stage = "completed"
        job.worker_id = None
        job.lease_expires_at = None

        db.commit()

        print(f"Job {research_id} completed successfully.")

    except Exception:
        db.rollback()
        raise 

    finally:
        db.close()
