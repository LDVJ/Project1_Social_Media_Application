from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from .db import Base,  engine, sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models
import psycopg2
from .schemas import create_user, user, update_user

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        print("DB connected Successfully")
        yield db
    finally:
        print('DB Disconnected')
        db.close()

app = FastAPI()

@app.post('/users', response_model=user, status_code=status.HTTP_201_CREATED)
def createUsers(user : create_user, db : Session = Depends(get_db)):
    new_user = models.users(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exsits")
    db.refresh(new_user)
    return new_user

@app.get('/users', response_model=List[user], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    output = db.query(models.users).all()
    return output

@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=user)
def unique_user(id : int, db: Session = Depends(get_db)):
    check = db.get(models.users, id)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found')
    user = db.query(models.users).filter(models.users.id == id).first()
    return user

@app.put('/users/{id}', status_code=status.HTTP_201_CREATED, response_model=user)
def updateUser(id: int, user : update_user, db: Session = Depends(get_db)):
    check = db.get(models.users, id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with ID: {id} not found")
    original = db.query(models.users).filter(models.users.id == id).first()
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

@app.delete('/users/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db : Session = Depends(get_db)):
    check = db.get(models.users, id)
    if not check(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User Not found')
    target =  db.query(models.users).filter(models.users.id == id).first()
    db.delete(target)
    db.commit()
