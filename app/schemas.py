from pydantic import BaseModel, EmailStr, condecimal
from typing import List
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

class ValidateUser(BaseModel):
    email : EmailStr
    password : str

class valid_token(BaseModel):
    access_token : str
    token_type : str

class token_data(BaseModel):
    id : str


class Create_prduct(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2, gt=0) #type: Ignore
    tags : List[str] | None = None
    currency : str | None = "USD"
    url : str | None = None




    #  id = Column(Integer,primary_key=True,nullable= False)
    # name = Column(String,nullable=False)
    # price = Column(NUMERIC(10,2),nullable=False)
    # created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    # currency = Column(Enum('USD',"INR","EUR","GBP", name="currency_enum"), nullable=False, default = "USD")
    # url = Column(Text, nullable=True)
    # tags = Column(JSON,nullable=True)