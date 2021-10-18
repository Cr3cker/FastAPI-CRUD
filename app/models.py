from datetime import datetime
from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    published: bool


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_on: datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_on: datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    class Config:
        orm_mode = True
