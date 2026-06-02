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

def find_post_index(id):
    for p in my_posts:
        if p['id']==id:
            return my_posts.index(p)
    return -1
@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}





@app.post('/createPosts',status_code=201)
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
    
@app.delete('/posts/{id}')
def delete_post(id:int):
    post=find_post_index(id)
    if post!=-1:
        my_posts.pop(post)
        return {"Success":"It was deleted"}
    raise HTTPException(status_code=404, detail="Post not found")

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    updated_post = post.dict()
    updated_post['id'] = id

    my_posts[index] = updated_post

    return {"data": updated_post}