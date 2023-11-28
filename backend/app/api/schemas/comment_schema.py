from pydantic import BaseModel


class add_comment(BaseModel):
    comment: str


class delete_comment(BaseModel):
    comment_id: int


class update_comment(delete_comment):
    new_comment: str
