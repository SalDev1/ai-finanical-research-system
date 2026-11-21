"""Task schemas."""
from enum import Enum
class TaskType(str, Enum):
    COMPANY_IDENTIFICATION = "company_identification"
    FINANCIAL_DATA = "financial_data"
    FINANCIAL_ANALYSIS = "financial_analysis"
    RISK_ANALYSIS = "risk_analysis"