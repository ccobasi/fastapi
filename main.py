from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}


@app.post("/createpost")
def get_posts(new_post: Post):
    print(new_post)
    return {"data": "new_post"}
