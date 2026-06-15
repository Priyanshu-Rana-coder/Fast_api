from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal
from .Schema import PostBase,PostCreate, PostResponse, UserCreate, UserOut
from . import utils
from .routers import user, post, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()





@app.get("/")
def home():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

