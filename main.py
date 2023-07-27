import os

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from db import Redis
from ws import ConnectionManager

app = FastAPI()
templates = Jinja2Templates(directory="templates")

dbconn = Redis()
try:
    dbconn.connect(os.environ["REDIS_URL"])
except:
    print("Unable to connect to Redis")
    exit(1)

manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/messages", response_class=JSONResponse)
async def messages():
    messages = await dbconn.get_messages()
    return messages


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            message = await ws.receive_text()
            await dbconn.add_message(message)
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(ws)
