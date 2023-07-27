import os

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import Redis
from ws import ConnectionManager

app = FastAPI()
templates = Jinja2Templates(directory="templates")

r = Redis()
r.connect(os.environ["REDIS_URL"])

manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            message = await ws.receive_text()
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(ws)
