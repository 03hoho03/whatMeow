from pydantic import BaseModel
from typing import Optional


class CatReturn(BaseModel):
    catName: str
    explain: Optional[str]
    gender: Optional[str]
    breed: Optional[str]
    ownerId: int
    id: int
