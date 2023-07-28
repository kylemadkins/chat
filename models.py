from pydantic import BaseModel


class User(BaseModel):
    username: str


class Message(BaseModel):
    username: str
    message: str
    type: str | None
