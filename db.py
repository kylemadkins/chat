import json

import redis.asyncio as redis

from models import Message


class Redis:
    _conn = None

    def connect(self, url: str):
        self._conn = redis.Redis.from_url(url)

    async def add_message(self, message: Message):
        await self._conn.rpush("messages", message.model_dump_json())

    async def get_messages(self) -> list[Message]:
        messages = await self._conn.lrange("messages", 0, -1)
        return [Message(**json.loads(m.decode("utf-8"))) for m in messages]
