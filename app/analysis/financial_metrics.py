from enum import Enum

class FinancialMetric(Enum):
    REVENUE_GROWTH = "revenue_growth"
    NET_INCOME_GROWTH = "net_income_growth"
    NET_PROFIT_MARGIN = "net_profit_margin"
    OPERATING_CASH_FLOW_MARGIN = "operating_cash_flow_margin"
    ASSET_GROWTH = "asset_growth"
    LIABILITY_GROWTH = "liability_growth"
    LIABILITY_TO_ASSET = "liability_to_asset"
    OPERATING_CASH_FLOW_TO_NET_INCOME = (
        "operating_cash_flow_to_net_income"
    )