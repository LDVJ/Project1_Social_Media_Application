from pydantic import BaseModel, EmailStr
from datetime import datetime

class create_user(BaseModel):
    name : str
    email: EmailStr
    password : str
    model_config = {
        'from_attributes': True
    }

class update_user(BaseModel):
    name : str | None = None
    password : str | None = None

class user(BaseModel):
    id : int
    name : str
    email: EmailStr
    created_at : datetime 
    model_config = {
        'from_attributes': True
    }
