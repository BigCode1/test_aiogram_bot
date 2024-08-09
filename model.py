import asyncio
import aiosqlite
from config import settings


async def create_model() -> None:
    async with aiosqlite.connect(settings.DB_PATH) as conn:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER)"""
        )
        await conn.commit()

        await conn.execute(
            "PRAGMA journal_mode=WAL"
        )
        await conn.commit()


async def insert_user(user_id: int, name: str, age: int) -> None:
    async with aiosqlite.connect(settings.DB_PATH) as conn:
        await conn.execute("INSERT OR IGNORE INTO users (user_id, name, age) VALUES (?, ?, ?)",
                           (user_id, name, age))
        await conn.commit()


async def all_users():
    async with aiosqlite.connect(settings.DB_PATH) as conn:
        cursor = await conn.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        return rows

if __name__ == "__main__":
    asyncio.run(create_model())
