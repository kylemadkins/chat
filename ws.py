import asyncio

from fastapi import WebSocket


class ConnectionManager:
    _connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self._connections.remove(ws)

    async def broadcast(self, message: str):
        await asyncio.gather(*[c.send_text(message) for c in self._connections])
