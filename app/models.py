from .db import Base
from sqlalchemy import Column, Integer, String, DateTime, NUMERIC, Text,Enum, JSON
from sqlalchemy.sql import func
from datetime import datetime

class users(Base):
    __tablename__  = 'users'

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    name = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,nullable= False)
    name = Column(String,nullable=False)
    price = Column(NUMERIC(10,2),nullable=False)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    currency = Column(Enum('USD',"INR","EUR","GBP", name="currency_enum"), nullable=False, default = "USD")
    url = Column(Text, nullable=True)
    tags = Column(JSON,nullable=True)

