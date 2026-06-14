from .. import models
from ..Schema import PostBase,PostCreate, PostResponse, UserCreate, UserOut
from .. import utils
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db


router=APIRouter(
    prefix='/posts'#/id
)
@router.get("/",response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/createPosts", status_code=201, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@router.delete("/{id}")
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


@router.put("/{id}",response_model=PostResponse)
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