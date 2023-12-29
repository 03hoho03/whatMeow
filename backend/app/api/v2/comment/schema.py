from pydantic import BaseModel
from datetime import datetime


class CommentAdd(BaseModel):
    comment: str


class CommentReturn(CommentAdd):
    id: int
    uploader: int
    postId: int
    nickname: str
    createdAt: datetime
