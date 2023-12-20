from pydantic import BaseModel


class GeneralUserReturn(BaseModel):
    email: str
    name: str
    nickname: str


class GeneralUserAdd(GeneralUserReturn):
    password: str
