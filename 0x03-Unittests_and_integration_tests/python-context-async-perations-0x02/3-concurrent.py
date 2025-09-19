import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        return results

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("All users:")
    print(results[0])
    print("\nUsers older than 40:")
    print(results[1])

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
