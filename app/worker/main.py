"""Worker entry point."""
import time 
import uuid
from app.worker.job_runner import (
    claim_next_job,
    process_job,
)
from app.db.session import get_db

WORKER_ID = f"worker-{uuid.uuid4()}"

# This worker runs independently of FastAPI.
def run_worker():
    """Run the background worker."""
    print(f"Starting worker : {WORKER_ID}.")
    while True:
        db = get_db()

        try :
            research_id = claim_next_job(db, WORKER_ID)
        except Exception as error:
            print(f"Job claiming failed: {error}")
            research_id = None

        finally:
            db.aclose()

        if research_id is None:
            time.sleep(3)
            continue

        try:
            process_job(research_id)

        except Exception as error:
            print(f"Job processing failed: {error}")

        time.sleep(1)

if __name__ == "__main__":
    run_worker()