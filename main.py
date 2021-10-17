from datetime import datetime
from typing import List
import databases
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy import create_engine, select, insert, delete
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts"

Base = declarative_base()

database = databases.Database(DATABASE_URL)


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    created_on = Column(DateTime, default=datetime.now())
    updated_on = Column(DateTime, default=datetime.now())


engine = create_engine(DATABASE_URL, echo=False)

Base.metadata.create_all(engine)


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


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/posts/', response_model=List)
async def get_posts():
    query = select(Posts)
    return await database.fetch_all(query)


@app.post('/posts/', response_model=Post)
async def create_post(post: PostIn):
    query = (
        insert(Posts).
            values(title=post.title, content=post.content, published=post.published,
                   created_on=datetime.now(),
                   updated_on=datetime.now())
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **post.dict()}


@app.delete('/posts/{post_id}')
async def delete_post(post_id: int):
    query = delete(Posts).where(Posts.id == post_id)
    await database.execute(query)
    return {"detail": "Post was deleted", "status_code": 204}
