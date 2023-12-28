from pydantic import BaseModel
from datetime import datetime


class GeneralUserBase(BaseModel):
    email: str


class GeneralUserReturn(GeneralUserBase):
    name: str
    nickname: str
    id: int


class GeneralUserAdd(GeneralUserBase):
    name: str
    nickname: str
    password: str


class GeneralUserLogin(GeneralUserBase):
    password: str


class UserPayload(BaseModel):
    id: int
    nickname: str
    exp: datetime
