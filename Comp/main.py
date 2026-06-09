from fastapi import FastAPI, Path, Response, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine,SessionLocal



models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host='localhost', database='FastAPi', user='postgres', password='prash741',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succes")
        break
    except Exception as error:
        print("Connection failed")
        print(error)
        time.sleep(2)



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
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}





@app.post('/createPosts',status_code=201)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": "created Post"}

@app.get('/posts/{id}')
def get_post(id :int, response: Response):
    cursor.execute("""SELECT * from posts WHERE posts.id=%s""",(id,))
    act_posts=cursor.fetchone()
    if act_posts:
        return {"post_detail":act_posts}
    else:
        #response.status_code=404
        #return {"post_detail":"Doesn't exists"}
        raise HTTPException(status_code=404,detail="Doesn't exists")
    
@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute(
        """
        DELETE FROM posts
        WHERE id = %s
        RETURNING *
        """,
        (id,)
    )

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return {"data": deleted_post}
@app.put('/posts/{id}')
def update_post(id: int, post: Post):

    cursor.execute(
        """
        UPDATE posts
        SET title = %s,
            content = %s,
            published = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, id)
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return {"data": updated_post}

@app.get("/sqlalchemy")
def test_posts(db: Session=Depends(get_db)):
    return {"Status":"Sucess"}