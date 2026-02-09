from fastapi import FastAPI
from .db import engine
from . import models
from .routes import users, authentication, product, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message':"welcome to fastapi platform"}

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(product.router)
app.include_router(post.router)