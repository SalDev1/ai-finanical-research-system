import asyncio

from sqlalchemy import text
from db.session import engine

async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("SELECT version();")
            )

            print("Database connected successfully!")
            print(result.scalar())

    except Exception as e:
        print("Database connection failed!")
        print(f"Error: {e}")

    finally:
        await engine.dispose()

async def check_database():
    async with engine.connect() as conn:

        result = await conn.execute(
            text("""
                SELECT
                    current_database(),
                    current_schema(),
                    inet_server_port()
            """)
        )

        print("Database connection:", result.fetchone())

        result = await conn.execute(
            text("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_name = 'research_jobs'
            """)
        )

        tables = result.fetchall()

        if tables:
            print("Research jobs table exists:", tables)
        else:
            print("Research jobs table NOT FOUND")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_database())