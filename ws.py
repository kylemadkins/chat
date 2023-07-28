import asyncio

from fastapi import WebSocket

from models import Message


class ConnectionManager:
    _connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self._connections.remove(ws)

    async def broadcast(self, message: Message):
        await asyncio.gather(
            *[c.send_json(message.model_dump()) for c in self._connections]
        )
