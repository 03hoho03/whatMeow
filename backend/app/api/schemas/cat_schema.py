from pydantic import BaseModel


class CatAdd(BaseModel):
    age: int = None
    breed: str = None
    catname: str
    gender: str = None
    explain: str = None
