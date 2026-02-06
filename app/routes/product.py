from fastapi import APIRouter, Depends, HTTPException, status
from ..db import get_db
from .. import schemas, models
from sqlalchemy.orm import Session



router = APIRouter()


@router.get("/products")
def get_all_prodct(db: Session = Depends(get_db)):
    all_posts = db.query(models)