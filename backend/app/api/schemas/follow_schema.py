from pydantic import BaseModel


class add_follow(BaseModel):
    to_follow: int


class delete_follow(BaseModel):
    to_unfollow: int
