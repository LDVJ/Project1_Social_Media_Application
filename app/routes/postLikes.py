from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2, schemas, models
from ..db import get_db
from typing import List,Dict, Any

router  = APIRouter(
    prefix= "/postslike/{post_id}",
    tags= ["PostLike"]
)

@router.get("/", response_model= List[schemas.PostLikes], status_code = status.HTTP_200_OK)
def post_likes(post_id: int, current_user : models.Users = Depends(oauth2.get_user_with_token), db: Session = Depends(get_db)):
    valid_post = db.query(models.Posts).filter(models.Posts.id  == post_id).first()
    if not valid_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No Post Found")
    get_post = db.query(models.PostLikes).filter(models.PostLikes.post_id == post_id).all() 
    return get_post


@router.get("/count", response_model= Dict[str, Any])
def like_count(post_id : int, db : Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_user_with_token)):
    valid_post = db.query(models.Posts).filter(models.Posts.id  == post_id).first()
    if not valid_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No Post Found")
    like_count = db.query(models.PostLikes).filter(models.PostLikes.post_id == post_id).count()
    return {"Total Likes": like_count}

@router.post("/", response_model= schemas.PostLikes, status_code=status.HTTP_200_OK)
def like_post(post_id : int, db : Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_user_with_token)):
    u_id = current_user.id
    new_like = models.PostLikes(user_id = u_id, post_id = post_id)
    try: 
        db.add(new_like)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post Already Liked")
    db.refresh(new_like)

    return new_like
    
    
