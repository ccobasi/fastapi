from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_posts = [{"title": "title 1", "content": "content 1", "id": 1},
            {"title": "title 2", "content": "content 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='123456', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was successfull!')
except Exception as error:
    print('Connection to database failed')
    print("Error:", error)


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def get_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """ DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return {"data": "Post was delete successfully"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
        returning *""",
        (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return {"data": updated_post}
