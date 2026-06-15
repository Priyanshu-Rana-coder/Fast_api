
from .. import models
from ..Schema import PostBase,PostCreate, PostResponse, UserCreate, UserOut
from .. import utils
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db

router=APIRouter(
    prefix='/users',
    tags=['Users']
)
@router.post("/", status_code=201,response_model=UserOut)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    #hash the pasword -user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}',response_model=UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user