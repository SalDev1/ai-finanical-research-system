"""Research schemas."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
from app.llm.llm_config import LLMConfig
from enum import Enum

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

class TaskType(str, Enum):
    COMPANY_IDENTIFICATION = "company_identification"
    FINANCIAL_DATA = "financial_data"
    FINANCIAL_ANALYSIS = "financial_analysis"
    RISK_ANALYSIS = "risk_analysis"

class ResearchTask(BaseModel):
   task_id : str
   task_type : Literal["company_identification","financial_data","finanical_analysis","risk_analysis"]
   objective : str
   inputs : dict
   expected_output : list[str]
   depends_on : list[str] = []
   required : bool = True
   llm_config: LLMConfig | None = None  

class ResearchTaskPlan(BaseModel):
    research_objective: str
    tasks: list[ResearchTask]