from pydantic import BaseModel, EmailStr, condecimal, HttpUrl, Field, StringConstraints
from typing import List, Literal,Annotated
from decimal import Decimal
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

class PostUserRelation(BaseModel):
    id: int
    title : str | None = None
    img_url : HttpUrl | None = None
    created_at : datetime
    updated_at : datetime | None = None

class UserPostRelation(BaseModel):
    id : int
    name : str
    email: EmailStr
    created_at : datetime
    user_posts : List[PostUserRelation] 
    model_config = {
        'from_attributes': True
    }

class UserData(BaseModel):
    id : int
    name : str
    email: EmailStr
    created_at : datetime
    # user_posts : List[PostUserRelation] 
    model_config = {
        'from_attributes': True
    }

class ValidateUser(BaseModel):
    email : EmailStr
    password : str

class valid_token(BaseModel):
    access_token : str
    token_type : str

class token_data(BaseModel):
    id : int

class create_product(BaseModel):
    name: str
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)] 
    tags : List[str] | None = None
    currency : Literal["USD","INR","EUR","GBP"] = "USD"
    url : HttpUrl | None = None

class product_details(create_product):
    id: int
    created_at : datetime
    updated_at : datetime | None = None

class update_product(BaseModel):
    name: str | None
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)] | None = None
    tags : List[str] | None = None 
    currency : Literal["USD","INR","EUR","GBP"] = "USD"
    url : HttpUrl | None = None


class CreatePost(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True)]
    content: str | None = None
    img_url: HttpUrl | None = None

class PostsData(CreatePost):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    owner: UserData
    model_config = {
        'from_attributes': True
    }

class UpdatePost(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)] | None = None
    content: Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)] | None = None
    img_url: HttpUrl | None = None

    model_config= {
        "from_attributes": True
    }

