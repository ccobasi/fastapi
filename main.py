from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


my_post = [{"title": "title 1", "content": "content 1", "id": 1},
           {"title": "title 2", "content": "content 2", "id": 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}


@app.post("/posts")
def get_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}
