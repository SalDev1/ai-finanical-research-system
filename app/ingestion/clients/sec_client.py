import httpx
from app.ingestion.company_registry import COMPANIES

class SECClient:
    BASE_URL = "https://data.sec.gov"
    def __init__(self):
        self.headers = {
            "User-Agent": "FinancialResearchSystem salthecoder11@gmail.com"
        }

    async def get_company_facts(self, cik: str):
        get_company_cik = COMPANIES.get(cik, {}).get("cik", "Unknown CIK")
        formatted_cik = str(get_company_cik).zfill(10)

        url = (
            f"{self.BASE_URL}/api/xbrl/companyfacts/"
            f"CIK{formatted_cik}.json"
        )

        async with httpx.AsyncClient(
            timeout=30.0,
            headers=self.headers
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()