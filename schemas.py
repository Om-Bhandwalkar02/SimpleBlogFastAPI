from fastapi.openapi.models import Schema
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    class Config:
        from_attributes = True