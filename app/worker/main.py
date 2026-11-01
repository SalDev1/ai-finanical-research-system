"""Worker entry point."""
import uuid
from app.worker.job_runner import (
    claim_next_job,
    process_job,
)
from app.db.session import AsyncSessionLocal, get_db
import asyncio


WORKER_ID = f"worker-{uuid.uuid4()}"

# This worker runs independently of FastAPI.
async def run_worker():
    """Run the background worker."""
    print(f"Starting worker : {WORKER_ID}.")
    while True:
        research_id = None
        try :
            async with AsyncSessionLocal() as db:
                 research_id = await claim_next_job(db, WORKER_ID)
        except Exception as error:
            print(f"Job claiming failed: {error}")
            research_id = None

        if research_id is None:
            await asyncio.sleep(3)
            continue

        print(f"Claimed research job: {research_id}")

        try:
           await process_job(research_id)

        except Exception as error:
            print(f"Job processing failed: {error}")

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_worker())