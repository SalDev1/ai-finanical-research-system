from enum import Enum

class FinancialMetric(Enum):
    REVENUE_GROWTH = "revenue_growth"
    NET_INCOME_GROWTH = "net_income_growth"
    ASSEST_GROWTH = "assets_growth"
    OPERATING_CASH_FLOW_MARGIN = "operating_cash_flow_margin"
    LIABILITY_GROWTH = "liability_growth"
    LIABILITY_TO_ASSET = "liability_to_asset"
    OPERATING_CASH_FLOW_TO_NET_INCOME = "operating_cash_flow_to_net_income"