"""Application entry point."""

from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Financial Research System",version="1.0.0", description="API for managing financial research jobs, tasks, and evidence records.")
app.include_router(api_router)

@app.get("/health/live")
def health_live():
    return {"status": "alive"}