from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from insurance_app import schemas, services
from insurance_app.database import get_db

router = APIRouter(
    prefix="/commissions",
    tags=["Commissions"]
)

@router.post("/", response_model=schemas.commission_schema.CommissionOut, status_code=status.HTTP_201_CREATED)
def create_commission(commission: schemas.commission_schema.CommissionCreate, db: Session = Depends(get_db)):
    return services.commission_service.create_commission(db, commission)

@router.get("/", response_model=List[schemas.commission_schema.CommissionOut])
def get_all_commissions(db: Session = Depends(get_db)):
    return services.commission_service.get_all_commissions(db)

@router.get("/{commission_id}", response_model=schemas.commission_schema.CommissionOut)
def get_commission(commission_id: int, db: Session = Depends(get_db)):
    db_commission = services.commission_service.get_commission_by_id(db, commission_id)
    if not db_commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    return db_commission

@router.put("/{commission_id}", response_model=schemas.commission_schema.CommissionOut)
def update_commission(commission_id: int, commission_update: schemas.commission_schema.CommissionUpdate, db: Session = Depends(get_db)):
    return services.commission_service.update_commission(db, commission_id, commission_update)

@router.delete("/{commission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commission(commission_id: int, db: Session = Depends(get_db)):
    services.commission_service.delete_commission(db, commission_id)
