from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from . import models
from .routes import users, authentication, product, post, postLikes, votes

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["http://localhost:8000",
          "https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials  = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.get('/')
def root():
    return {'message':"welcome to fastapi platform"}

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(product.router)
app.include_router(post.router)
app.include_router(postLikes.router)
app.include_router(votes.router)