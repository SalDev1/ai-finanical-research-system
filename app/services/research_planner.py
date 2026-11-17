from app.llm.llm_client import LLMClient
# ResearchPlanner is dependent on LLMClient
class ResearchPlanner:
    def __init__(self, llm_client : LLMClient):
        self.llm_client = llm_client
        
    async def create_plan(self, question : str) -> dict:
        response = await self.llm_client.generate_research_plan(question)
        return response