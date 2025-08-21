from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from insurance_app.schemas.premium_schema import PremiumCreate, PremiumUpdate, PremiumResponse
from insurance_app.services.premium_service import PremiumService
from insurance_app.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PremiumResponse)
def create_premium(premium: PremiumCreate, db: Session = Depends(get_db)):
    service = PremiumService(db)
    return service.create_premium(premium)

@router.get("/", response_model=List[PremiumResponse])
def list_premiums(db: Session = Depends(get_db)):
    service = PremiumService(db)
    return service.get_all_premiums()

@router.get("/{premium_id}", response_model=PremiumResponse)
def get_premium(premium_id: uuid.UUID, db: Session = Depends(get_db)):
    service = PremiumService(db)
    premium = service.get_premium_by_id(premium_id)
    if not premium:
        raise HTTPException(status_code=404, detail="Premium not found")
    return premium

@router.put("/{premium_id}", response_model=PremiumResponse)
def update_premium(premium_id: uuid.UUID, premium_data: PremiumUpdate, db: Session = Depends(get_db)):
    service = PremiumService(db)
    updated_premium = service.update_premium(premium_id, premium_data)
    if not updated_premium:
        raise HTTPException(status_code=404, detail="Premium not found")
    return updated_premium

@router.delete("/{premium_id}")
def delete_premium(premium_id: uuid.UUID, db: Session = Depends(get_db)):
    service = PremiumService(db)
    service.delete_premium(premium_id)
    return {"message": "Premium deleted successfully"}
