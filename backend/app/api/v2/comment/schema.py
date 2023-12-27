from pydantic import BaseModel


class CommentAdd(BaseModel):
    comment: str


class CommentReturn(CommentAdd):
    id: int
    uploader: int
    postId: int
