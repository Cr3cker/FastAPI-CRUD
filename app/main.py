from datetime import datetime
from app.models import Post, PostIn
from app.db import Base, Posts, engine, database
from typing import List, Dict
from fastapi import FastAPI
from sqlalchemy import select, insert, delete, update

Base.metadata.create_all(engine)

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
    result = await database.fetch_all(query)
    if result is not None:
        return result
    else:
        return {"detail": "No posts in the database"}


@app.get('/posts/{post_id}', response_model=Dict)
async def get_single_post(post_id: int):
    query = select(Posts).where(Posts.id == post_id)
    result = await database.fetch_one(query)
    if result is not None:
        return result
    else:
        return {"detail": "No such post found"}


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


@app.put('/posts/{post_id}')
async def update_post(post_id: int, post: PostIn):
    query = (
        update(Posts).
            where(Posts.id == post_id).
            values(title=post.title, content=post.content, published=post.published,
                   updated_on=datetime.now())
    )
    await database.execute(query)
    return {"detail": f"Post {post_id} updated successfully!"}


@app.delete('/posts/{post_id}', response_model=Dict)
async def delete_post(post_id: int):
    available_id = select(Posts.id)
    result = await database.fetch_all(available_id)
    for dict_ in result:
        if dict_.get("id") == post_id:
            query = delete(Posts).where(Posts.id == post_id)
            await database.execute(query)
            return {"detail": "Post was deleted", "status_code": 204}
        else:
            return {"detail": "No such post found"}
