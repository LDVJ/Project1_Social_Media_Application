from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from ..db import get_db
from .. import utilities, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login") 
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session =Depends(get_db)):
    credentials_check = db.query(models.users).filter(models.users.email == user_creds.username).first()
    if credentials_check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utilities.verify_hash_password(user_creds.password, credentials_check.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    access_token = oauth2.create_jwt_token({'user_id':credentials_check.id})
    # print(access_token)
    return {"access_token":access_token,"token_type":"bearer"}