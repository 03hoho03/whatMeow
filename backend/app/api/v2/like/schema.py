from pydantic import BaseModel


class ApplyLike(BaseModel):
    version: int
