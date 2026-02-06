from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
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

        id : str = payload.get("user_id") # it is the key of the data we send during the encoding process
        
        if id is None: 
            raise credential_exception
        token_data = schemas.token_data(id = id)
    except JWTError:
        credential_exception


def get_user_with_token(token: str  = Depends(oauth2_schema)):
    credential_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised access", headers={"WWW-Authenticate":"Bearer"})

    return verify_jwt_token(token=token,credential_exception=credential_exception)
    
