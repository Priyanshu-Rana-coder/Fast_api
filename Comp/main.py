from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal
from .Schema import PostBase,PostCreate, PostResponse, UserCreate, UserOut
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts",response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/createPosts", status_code=201, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Deleted successfully"}


@app.put("/posts/{id}",response_model=PostResponse)
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return post_query.first()


@app.post("/users", status_code=201,response_model=UserOut)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user