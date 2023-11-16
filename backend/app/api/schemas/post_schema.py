from pydantic import BaseModel


class PostDetail(BaseModel):
    post_id: int
