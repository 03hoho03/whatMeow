from pydantic import BaseModel
from datetime import datetime


class GeneralUserBase(BaseModel):
    email: str


class GeneralUserReturn(GeneralUserBase):
    name: str
    nickname: str
    id: int


class GeneralUserAdd(GeneralUserReturn):
    password: str


class GeneralUserLogin(GeneralUserBase):
    password: str


class UserPayload(BaseModel):
    id: int
    nickname: str
    username: str
    exp: datetime
