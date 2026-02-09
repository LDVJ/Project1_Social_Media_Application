from fastapi import APIRouter, Depends, HTTPException, status
from ..db import get_db
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List



router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[schemas.product_details], status_code=status.HTTP_200_OK)
def get_all_prodct(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_user_with_token)):
    print(current_user.email)
    all_posts = db.query(models.Products).all()
    return all_posts

@router.post("/", response_model=schemas.product_details, status_code=status.HTTP_201_CREATED)
def ceate_product(product: schemas.create_product,db: Session = Depends(get_db), get_user_id : int = Depends(oauth2.get_user_with_token)):
    product_data = product.model_dump(exclude_unset=True)
    if product_data.get("url"):
        product_data["url"] = str(product_data["url"])
    new_product = models.Products(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/{id}", response_model= schemas.product_details, status_code=status.HTTP_200_OK)
def unique_product(id : int, db: Session = Depends(get_db), get_user_id: int = Depends(oauth2.get_user_with_token)):
    check_product = db.query(models.Products).filter(models.Products.id  == id).first()
    if check_product is None: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No product found")
    return check_product

@router.put("/{id}", response_model=schemas.product_details, status_code=status.HTTP_201_CREATED)
def prouct_update(id: int, product: schemas.update_product, db: Session = Depends(get_db), get_user_id: int = Depends(oauth2.get_user_with_token)):
    check_product = db.query(models.Products).filter(models.Products.id == id).first()
    if check_product is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No prouct found for updating")
    product_dict = product.model_dump(exclude_unset=True)

    if product_dict is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid Input")
    
    if product_dict.get("url") is not None:
        product_dict["url"] = str(product_dict["url"])
    
    for key, value in product_dict.items():
        setattr(check_product, key, value) 

    db.commit()
    db.refresh(check_product)

    return check_product

@router.delete('/{id}')
def delete_product(id: int, db: Session = Depends(get_db), get_user_id: int = Depends(oauth2.get_user_with_token)):
    check_product = db.query(models.Products).filter(models.Products.id == id).first()
    if check_product is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No Product found")
    db.delete(check_product)
    db.commit()

    return {"message":"Product Deleted successfully"}
    

