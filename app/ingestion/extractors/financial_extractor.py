"""Financial data extractor."""
class FinancialExtractor:
    # Fetching financial metrics from the SEC company facts data using predefined tags.
    METRIC_TAGS = {
        "revenue": [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
        ],
        "net_income": [
            "NetIncomeLoss"
        ],
        "total_assets": [
            "Assets"
        ],
        "total_liabilities": [
            "Liabilities"
        ],
        "operating_cash_flow": [
            "NetCashProvidedByUsedInOperatingActivities"
        ]
    }

    def extract(self, company_facts):
        # This func extracts all the financial metrics of the particular asked company.
        facts = company_facts["facts"]["us-gaap"]
        extracted = {}
        for metric, possible_tags in self.METRIC_TAGS.items():
            for tag in possible_tags:
                if tag in facts:
                    extracted[metric] = facts[tag]
                    break

        return extracted