from datetime import date, datetime

from app.ingestion.validators.financial_validators import FinancialValidator
class FinancialExtractor:
    # Fetching financial metrics from the SEC company facts data using predefined tags.
    financial_validator = FinancialValidator()

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

    METRIC_TYPES = {
        "revenue": "duration",
        "net_income": "duration",
        "operating_cash_flow": "duration",
        "total_assets": "instant",
        "total_liabilities": "instant",
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

    def normailze_finanical_facts(self, extracted_facts): 
        # This func normalizes the extracted financial metrics into a structured format.
        normalized_records = []
        for metric, fact_data in extracted_facts.items():
            period_type = self.METRIC_TYPES.get(metric)

            if not period_type:
                continue

            unit = fact_data["units"]

            for observation in fact_data["units"]['USD']:

                # Only annual filings for our first version
                if observation.get("form") != "10-K":
                    continue

                start = observation.get("start")
                end = observation.get("end")

                if not end:
                    continue

                # Duration metrics: approximately one fiscal year
                if period_type == "duration":

                    if not start:
                        continue

                    start_date = date.fromisoformat(start)
                    end_date = date.fromisoformat(end)

                    duration = (end_date - start_date).days

                    if not 330 <= duration <= 380:
                        continue

                # Instant metrics: no start date
                elif period_type == "instant":

                    if start:
                        continue

                start_date = datetime.fromisoformat(start) if start else None
                end_date = datetime.fromisoformat(end) if end else None
                filling_date = datetime.fromisoformat(observation.get("filed")) if observation.get("filed") else None

                record = {
                    "metric": metric,
                    "value": observation["val"],
                    "unit": 'USD',
                    "period_type": period_type,
                    "period_start": start_date,
                    "period_end": end_date,
                    "fiscal_year": observation.get("fy"),
                    "fiscal_period": observation.get("fp"),
                    "filing_type": observation.get("form"),
                    "filing_date": filling_date,
                    "accession_number": observation.get("accn"),
                    "source": "SEC EDGAR",
                }

                if not self.financial_validator.validate(record):
                    continue

                normalized_records.append(record)
        return normalized_records