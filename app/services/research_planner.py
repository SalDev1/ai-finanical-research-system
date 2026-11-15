from app.llm.base import LLMClient

# ResearchPlanner is dependent on LLMClient
class ResearchPlanner:

    def __init__(self, llm_client : LLMClient):
        self.llm_client = llm_client

    async def create_plan(self, question : str) -> dict:
        return await self.llm_client.generate_research_plan(question)