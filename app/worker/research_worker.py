import asyncio

from app.llm.hugging_face_client import HuggingFaceLLMClient
from app.services.research_planner import ResearchPlanner

llm_huggingface_client = HuggingFaceLLMClient()
planner = ResearchPlanner(llm_huggingface_client)

async def run_research(question : str) : 
    plan = await planner.create_plan(question)
    print("Research Plan ");
    print(f"{plan}")

if __name__ == "__main__" :
    asyncio.run(
        run_research(
            "How has Apple's revenue grown over the last 5 years?"
        )
    )