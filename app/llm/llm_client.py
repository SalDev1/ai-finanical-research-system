from abc import abstractmethod
class LLMClient():
    @abstractmethod
    # This helps me generate a research plan based on the user's intent so our application engine understands it. 
    async def generate_research_plan(
        self,
        question: str
    ) -> dict:
        """
        Generate a structured research plan
        from the user's financial question.
        """
        pass
       