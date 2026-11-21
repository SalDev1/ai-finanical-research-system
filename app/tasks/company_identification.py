from app.llm.llm_config import LLM_TASK_CONFIGS
from app.schemas.research import ResearchTask

class CompanyIdentificationExecutor:
    def __init__(self, llm_client_factory):
        self.llm_client_factory = llm_client_factory

    def build_company_identification_prompt(self, task):
            return ""

    async def execute(self, task : ResearchTask):

        config = LLM_TASK_CONFIGS["company_identification"]
        client = self.llm_client_factory.create(config)
        result = await client.generate(
            prompt=self.build_company_identification_prompt(task)
        )
        return result
