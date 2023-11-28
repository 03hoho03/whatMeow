from pydantic import BaseModel


class ResourceId(BaseModel):
    id: int

    class Config:
        from_attributes = True
