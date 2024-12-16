import aiosqlite as sql
import json
import asyncio


async def main():
    with open("config.json", 'r') as file:
        data = json.load(file)
    items = ",".join(item+" INTEGER DEFAULT 0 NOT NULL" for item in data["Items"])
    async with sql.connect("data.db") as conn:
        async with conn.cursor() as cu:
            await cu.execute(f"CREATE TABLE IF NOT EXISTS items(user_id INTEGER UNIQUE NOT NULL, {items})")
            await conn.commit()

async def add_user_item(user_id: int, item: str):
    async with sql.connect("data.db") as conn:
        async with conn.cursor() as cu:
            await cu.execute(f'INSERT INTO items (user_id, {item}) VALUES ({user_id}, 1) ON CONFLICT (user_id) DO UPDATE SET {item}={item}+1')
            await conn.commit()

async def get_user_item_count(user_id: int, item: str) -> int:
    async with sql.connect("data.db") as conn:
        async with conn.cursor() as cu:
            await cu.execute(f"SELECT {item} FROM items WHERE user_id={user_id}")
            result = await cu.fetchone()
            return result[0] if result else 0

async def decrease_user_item_count(user_id: int, item: str, count: int = 1) -> None:
    async with sql.connect("data.db") as conn:
        async with conn.cursor() as cu:
            await cu.execute(f'UPDATE items SET {item}={item}-{count} WHERE user_id={user_id}')
            await conn.commit()

async def get_config_data():
    with open('data.json', 'r') as file:
        return json.load(file)