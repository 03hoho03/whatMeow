from pydantic import BaseModel


class SearchFollower(BaseModel):
    start: int
    limit: int


class SearchHashTag(SearchFollower):
    hashtag: str


class SearchName(SearchFollower):
    name: str
