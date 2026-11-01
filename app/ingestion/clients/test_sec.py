import asyncio
from sec_client import SECClient

async def main():
    sec_client = SECClient()
    data = await sec_client.get_company_facts(
        "0000320193"
    )
    print(data["entityName"])
    print(data["facts"]["us-gaap"].keys())

if __name__ == "__main__":
    asyncio.run(main())