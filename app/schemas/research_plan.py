"""Research schemas."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class ResearchTask(BaseModel):
   task_id : str
   task_type : Literal["company_identification","financial_data","finanical_analysis","risk_analysis"]
   description : str
   required : bool = True


class ResearchPlan(BaseModel):
   company_name : str
   ticker : str | None = None
   research_type : str
   period : str | None = None 
   tasks : list[ResearchTask]