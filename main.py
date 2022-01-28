from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}


@app.post("/createpost")
def get_posts():
    return {"message": "Successfully created a post."}
