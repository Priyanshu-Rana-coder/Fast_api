from fastapi import FastAPI, Path, Response, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]=None


my_posts=[{"title": "title of post1","content":"content of post1","id":1221},{"title":"fav food", "content":"Pizza","id":1111}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
    return {}


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}





@app.post('/createPosts')
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,10**10)
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get('/posts/{id}')
def get_post(id :int, response: Response):
    act_posts=find_post(id)
    if act_posts:
        return {"post_detail":act_posts}
    else:
        #response.status_code=404
        #return {"post_detail":"Doesn't exists"}
        raise HTTPException(status_code=404,detail="Doesn't exists")