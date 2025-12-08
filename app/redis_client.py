import os

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()


class RedisClient:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = None

    async def connect(self):
        if not self.client:
            self.client = await redis.from_url(self.redis_url, decode_responses=True)
        return self.client

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None

    async def get(self, key: str):
        client = await self.connect()
        return await client.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        client = await self.connect()
        if expire:
            await client.setex(key, expire, value)
        else:
            await client.set(key, value)

    async def delete(self, key: str):
        client = await self.connect()
        await client.delete(key)

    async def delete_pattern(self, pattern: str):
        client = await self.connect()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)


redis_client = RedisClient()
