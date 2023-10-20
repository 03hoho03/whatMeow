from pydantic import BaseModel


class PostUpload(BaseModel):
    title: str


class HashTagUpload(BaseModel):
    hashtag: list
