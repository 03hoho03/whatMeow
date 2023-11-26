from pydantic import BaseModel
from typing import List


class CatAdd(BaseModel):
    age: int = None
    breed: str = None
    catname: str = None
    gender: str = None
    explain: str = None
    hashtag: List[str] = None


class CatUpdateName(BaseModel):
    cat_id: int
    catname: str


class CatUpdateExplain(BaseModel):
    cat_id: int
    explain: str
