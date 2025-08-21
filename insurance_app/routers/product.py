from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from insurance_app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from insurance_app.services.product_service import ProductService
from insurance_app.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create_product(product)

@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: uuid.UUID, product_data: ProductUpdate, db: Session = Depends(get_db)):
    service = ProductService(db)
    updated_product = service.update_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.delete_product(product_id)
    return {"message": "Product deleted successfully"}
