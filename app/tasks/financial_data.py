from app.llm.llm_config import LLM_TASK_CONFIGS
from app.schemas.research import ResearchTask

class FinancialDataExecutor:
    def __init__(self, llm_client_factory):
        self.llm_client_factory = llm_client_factory

    def build_financial_data_prompt(self, task):
            return ""

    async def execute(self, task : ResearchTask):

        config = LLM_TASK_CONFIGS["financial_data"]
        client = self.llm_client_factory.create(config)
        result = await client.generate(
            prompt=self.build_financial_data_prompt(task)
        )
        return result
