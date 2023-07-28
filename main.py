import os

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import Redis
from ws import ConnectionManager
from models import User, Message

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


@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    username = request.cookies.get("X-Authorization")
    if username:
        return templates.TemplateResponse("chat.html", {"request": request})
    return RedirectResponse("/")


@app.post("/join")
def join(user: User, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


@app.get("/messages")
async def messages(request: Request, response: Response) -> list[Message]:
    username = request.cookies.get("X-Authorization")
    if username:
        messages = await dbconn.get_messages()
        return messages
    response.status_code = status.HTTP_401_UNAUTHORIZED


@app.websocket("/ws")
async def ws(ws: WebSocket):
    username = ws.cookies.get("X-Authorization")
    if username:
        await manager.connect(ws)
        resp = Message(username=username, message="joined", type="event")
        await manager.broadcast(resp)
        try:
            while True:
                message = await ws.receive_text()
                resp.message = message
                resp.type = "message"
                await dbconn.add_message(resp)
                await manager.broadcast(resp)
        except WebSocketDisconnect:
            manager.disconnect(ws)
            resp.message = "left"
            resp.type = "event"
            await manager.broadcast(resp)
