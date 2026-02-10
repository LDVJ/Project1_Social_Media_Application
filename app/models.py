from .db import Base
from sqlalchemy import Column, Integer, String, DateTime, NUMERIC, Text,Enum, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__  = 'users'

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    name = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user_posts = relationship("Posts", back_populates="owner", cascade= "all, delete")

class Posts(Base):
    __tablename__ = "posts"

    id =  Column(Integer, primary_key=True, nullable= False, index=True)
    title = Column(String,nullable=False)
    content = Column(String, nullable=True)
    img_url = Column(Text,nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("Users", back_populates="user_posts")
    # owner = relationship("Users",back_populates="posts")

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

class PostLikes(Base):
    __tablename__ = "post_likes"

    id =  Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), nullable = False)

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name = "unique_post_like"),
    )

