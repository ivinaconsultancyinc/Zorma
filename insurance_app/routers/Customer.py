from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from insurance_app import models, schemas
from insurance_app.database import get_db
from insurance_app.services import customer_service

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post("/", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, customer)

@router.get("/", response_model=List[schemas.CustomerOut])
def get_all_customers(db: Session = Depends(get_db)):
    return customer_service.get_all_customers(db)

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.get_customer_by_id(db, customer_id)

@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    return customer_service.update_customer(db, customer_id, customer)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer_service.delete_customer(db, customer_id)
    return 