from pydantic import BaseModel
from typing import List
from fastapi import UploadFile


class PostUpload(BaseModel):
    title: str
    hashtag: str
    images: List[UploadFile]
