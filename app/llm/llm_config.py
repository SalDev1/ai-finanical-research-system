from pydantic import BaseModel 
from app.schemas.tasks import TaskType

class LLMConfig(BaseModel):
    name: str
    provider: str
    model: str
    temperature: float = 0.1
    max_tokens: int = 2000

LLM_TASK_CONFIGS = {
    "company_identification": LLMConfig(
        name="company_identification",
        provider="huggingface",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        temperature=0.1,
        max_tokens=200,
    ),
    "financial_analysis": LLMConfig(
        name="financial_analysis",
        provider="huggingface",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        temperature=0.2,
        max_tokens=200,
    ),
    "risk_analysis": LLMConfig(
        name="risk_analysis",
        provider="huggingface",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        temperature=0.2,
        max_tokens=200,
    ),
    "financial_data": LLMConfig(
        name="financial_data",
        provider="huggingface",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        temperature=0.1,
        max_tokens=200,
    ),
}

