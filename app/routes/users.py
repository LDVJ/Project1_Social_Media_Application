from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db import get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utilities

router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)

@router.post('/', response_model=schemas.UserData, status_code=status.HTTP_201_CREATED)
def createUsers(user : schemas.create_user, db : Session = Depends(get_db)):
    hash_password = utilities.create_hash_password(user.password)
    user.password = hash_password
    user.email = user.email.lower()
    added_user = models.Users(**user.model_dump(exclude_unset=True))
    db.add(added_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exsits")
    db.refresh(added_user)
    return added_user

@router.get('/', response_model=List[schemas.UserPostRelation], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    output = db.query(models.Users).options(joinedload(models.Users.user_posts)).all()
    return output

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserData)
def unique_user(id : int, db: Session = Depends(get_db)):
    check = db.get(models.Users, id)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found')
    user = db.query(models.Users).filter(models.Users.id == id).first()
    return user

@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UserData)
def updateUser(id: int, user : schemas.update_user, db: Session = Depends(get_db)):
    check = db.get(models.Users, id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with ID: {id} not found")
    original = db.query(models.Users).filter(models.Users.id == id).first()
    updated_user = user.model_dump(exclude_unset=True)
    update_data = {k: v for k,v in updated_user.items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Update: Values can't be null")
    
    for key, value in updated_user.items():
        setattr(original, key, value)

    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Update: Values can't be null")
    db.refresh(original)
    return original

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db : Session = Depends(get_db)):
    check = db.get(models.Users, id)
    if not check(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User Not found')
    target =  db.query(models.Users).filter(models.Users.id == id).first()
    db.delete(target)
    db.commit()
    return 

# @router.post("/login", status_code = status.HTTP_200_OK, response_model=schemas.user)
# def authenticate_user(user: schemas.ValidateUser,db: Session = Depends(get_db)):
#     check = db.query(models.users).filter(models.users.email == user.email).first()
#     if check is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not found')
#     if not utilities.verify_hash_password(user.password, check.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Password doesn't match")
#     return check