import redis.asyncio as redis


class Redis:
    _conn = None

    def connect(self, url: str):
        self._conn = redis.Redis.from_url(url)

    async def add_message(self, message: str):
        await self._conn.rpush("messages", message)

    async def get_messages(self) -> str:
        messages = await self._conn.lrange("messages", 0, -1)
        return messages
