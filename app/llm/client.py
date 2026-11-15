from app.llm.base import LLMClient 

class OpenAIClient(LLMClient):

    def __init__(self, api_key:str):
        self.api_key = api_key

    async def generate_research_plan(self, question : str) -> dict:
        # OpenAI call will go here.
        return {
            "question" : question,
            "tasks": []
        }
        