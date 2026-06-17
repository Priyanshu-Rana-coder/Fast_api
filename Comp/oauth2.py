from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import Schema, database, models
from fastapi import Depends, status,HTTPException
from  fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = "8f4c7d2b1a9e6f3c5d8e1a7b9c2f4d6e8a1b3c5d7f9e2a4c6b8d1f3e5a7c9b2d"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=Schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=401,headers={"WWW-Authenticate":"Bearer"})
    
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    
    return  user
