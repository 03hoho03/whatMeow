from pydantic import BaseModel
from datetime import datetime


class GeneralUserAdd(BaseModel):
    email: str
    name: str
    nickname: str
    password: str


class KaKaoUserAdd(BaseModel):
    nickname: str
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


class UpdateNickname(BaseModel):
    nickname: str


class UpdateName(BaseModel):
    name: str


class UpdateExplain(BaseModel):
    explain: str
