"""Research schemas."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
from app.llm.llm_config import LLMConfig

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

class ResearchTask(BaseModel):
   task_id : str
   task_type : Literal["company_identification","financial_data","finanical_analysis","risk_analysis"]
   description : str
   required : bool = True
   llm_config: LLMConfig | None = None

class ResearchTaskPlan(BaseModel):
   company_name : str
   ticker : str | None = None
   research_type : str
   period : str | None = None 
   tasks : list[ResearchTask]