from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, db, models
from sqlalchemy.orm  import Session
from fastapi.security import oauth2
from fastapi import Depends, HTTPException, status

oauth2_schema = oauth2.OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "82f844718740a939a0e6f040a0ea8441"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt, expire

def verify_jwt_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get("user_id") # it is the key of the data we send during the encoding process     
        if user_id is None: 
            raise credential_exception
        token_data = schemas.token_data(id = user_id)

    except JWTError:
        raise credential_exception

    return token_data


def get_user_with_token(beared_token: str  = Depends(oauth2_schema), db: Session = Depends(db.get_db)):
    print("user token ", beared_token  )
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised access", headers={"WWW-Authenticate":"Bearer"})

    token = verify_jwt_token(token=beared_token,credential_exception=credential_exception)  

    user_data = db.query(models.users).filter(models.users.id == token.id).first()
    print(user_data)
    return user_data

    

