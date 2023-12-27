from pydantic import BaseModel


class PostReturn(BaseModel):
    id: int
    uploaderId: int
    title: str
