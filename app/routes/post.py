from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, db, oauth2, models
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[schemas.PostsData], status_code = status.HTTP_200_OK)
def get_all_post(user : dict = Depends(oauth2.get_user_with_token), db : Session = Depends(db.get_db)):
    all_posts = db.query(models.Posts).all()
    return all_posts

@router.post("/", response_model=schemas.PostsData, status_code = status.HTTP_201_CREATED)
def create_post(payload: schemas.CreatePost, db : Session = Depends(db.get_db), user : dict = Depends(oauth2.get_user_with_token)):
    payload_dict = payload.model_dump(exclude_unset=True)
    if payload_dict.get("img_url"):
        payload_dict["img_url"] = str(payload_dict["img_url"])
    # payload_dict["user_id"] = user.get("id")
    new_post = models.Posts(**payload_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put("/{id}", response_model = schemas.PostsData, status_code = status.HTTP_201_CREATED)
def upate_post(id: int, payload: schemas.UpdatePost, db : Session = Depends(db.get_db), user : dict = Depends(oauth2.get_user_with_token)):
    orignal_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if orignal_post is None: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Post not found")
    updated_data = payload.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No Data for updating is provided")
    if updated_data.get("img_url"):
        updated_data["img_url"] = str(updated_data["img_url"])
    for key, value in updated_data.items():
        setattr(orignal_post, key, value)
    
    db.commit()
    db.refresh(orignal_post)

    return orignal_post

@router.get("/{id}", response_model=schemas.PostsData, status_code=status.HTTP_200_OK)
def get_a_post(id: int, db: Session = Depends(db.get_db), user  : dict = Depends(oauth2.get_user_with_token)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(db.get_db), user  = Depends(oauth2.get_user_with_token)):
    get_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if get_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No Post Found")
    db.delete(get_post)
    db.commit()

    return None
