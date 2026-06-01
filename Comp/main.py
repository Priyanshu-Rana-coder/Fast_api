from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]=None


my_posts=[{"title": "title of post1","content":"content of post1","id":1221},{"title":"fav food", "content":"Pizza","id":1111}]


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}





@app.post('/createPosts')
def create_posts(post: Post):
    my_posts.append(post.dict())
    return {"data": "new Post"}