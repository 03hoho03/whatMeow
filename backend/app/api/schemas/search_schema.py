from pydantic import BaseModel


class SearchHashTag(BaseModel):
    hashtag: str
    start: int
    limit: int


class SearchName(BaseModel):
    name: str
