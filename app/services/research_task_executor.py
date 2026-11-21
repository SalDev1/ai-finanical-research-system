from app.schemas.tasks import TaskType
from app.llm.llm_config import LLM_TASK_CONFIGS, LLMConfig
from app.schemas.research import ResearchTask
from abc import abstractmethod

from app.tasks.company_identification import CompanyIdentificationExecutor
from app.tasks.financial_analysis import FinancialAnalysisExecutor
from app.tasks.financial_data import FinancialDataExecutor
from app.tasks.risk_analysis import RiskAnalysisExecutor

# This class is responsible where Python assigns task to an executor.

EXECUTORS = {
    TaskType.COMPANY_IDENTIFICATION:
        CompanyIdentificationExecutor,

    TaskType.FINANCIAL_DATA:
        FinancialDataExecutor,

    TaskType.FINANCIAL_ANALYSIS:
        FinancialAnalysisExecutor,

    TaskType.RISK_ANALYSIS:
        RiskAnalysisExecutor,
}

class ResearchTaskConfigurationResolver:
    def resolve(self, task_type: TaskType) -> LLMConfig | None:
        mapping = {
            TaskType.FINANCIAL_ANALYSIS:
                LLM_TASK_CONFIGS["financial_analysis"],

            TaskType.RISK_ANALYSIS:
                LLM_TASK_CONFIGS["risk_analysis"],
        }
        return mapping.get(task_type)


class ResearchTaskExecutor:
    def __init__(self, llm_client_factory):
        self.llm_client_factory = llm_client_factory

    @abstractmethod
    async def execute(self, task: ResearchTask):
        executor_class = EXECUTORS[task.task_type]
        executor = executor_class(self.llm_client_factory)
        result = await executor.execute(task)
        print(f"executed tasks {result}")
        return result
