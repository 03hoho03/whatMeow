from pydantic import BaseModel


class SearchHashTag(BaseModel):
    hashtag: str
    start: int
    limit: int


class SearchName(BaseModel):
    name: str
    start: int
    limit: int


class SearchFollower(BaseModel):
    user_id: int
    start: int
    limit: int
