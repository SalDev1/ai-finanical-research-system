"""Research schemas."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    question: str = Field(min_length=10, max_length=500)
    research_type: Literal["general_finance","company_analysis","market_analysis","macro_analysis","fund_analysis"]
    depth : Literal["standard","deep"] = "deep"
    period : str | None = None
    region : str | None = None 


class ResearchResponse(BaseModel):
    research_id: UUID 
    status: str
    message: str

class ResearchStatusResponse(BaseModel):
    research_id: UUID
    status: str
    current_stage: str
    created_at: datetime
    updated_at: datetime