from pydantic import BaseModel
from datetime import datetime


class GeneralUserAdd(BaseModel):
    email: str
    name: str
    username: str
    password: str


class KaKaoUserAdd(BaseModel):
    username: str


class User(KaKaoUserAdd):
    id: int

    class Config:
        from_attributes = True


class LoginUser(BaseModel):
    email: str
    password: str


class UserPayload(User):
    exp: datetime
