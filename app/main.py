from turtle import title
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status, Depends

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
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

    # posts = db.query(models.Post).all()
    posts = db.query(models.Post)
    return posts


@app.get("/posts")
# def get_posts():
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def get_posts(post: Post):
def get_posts(post: schemas.PostBase, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}")
# def get_posts(id:int):
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

    return {"data": "Post was delete successfully"}


@app.put("/posts/{id}")
# def update_post(id: int, post:Post):
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    #     returning *""",
    #     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.PostCreate).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # return {"data": updated_post}
    return post_query.first()
