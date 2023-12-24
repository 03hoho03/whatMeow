from pydantic import BaseModel


class PostReturn(BaseModel):
    id: int
    uploader_id: int
    title: str
