from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, Schema, models, utils


router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(userCredentials:Schema.UserLogin,   db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==userCredentials.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Wrong Credentials"
        )
    if not utils.verify(userCredentials.password,user.password):
        raise HTTPException(
            status_code=404,
            detail="Wrong Credentials"
        )
    return {'token':"example token"}
