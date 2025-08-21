from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from insurance_app import models, schemas

def create_commission(db: Session, commission: schemas.commission_schema.CommissionCreate):
    db_commission = models.commission.Commission(**commission.dict())
    db.add(db_commission)
    db.commit()
    db.refresh(db_commission)
    return db_commission

def get_all_commissions(db: Session):
    return db.query(models.commission.Commission).all()

def get_commission_by_id(db: Session, commission_id: int):
    return db.query(models.commission.Commission).filter(models.commission.Commission.id == commission_id).first()

def update_commission(db: Session, commission_id: int, commission_update: schemas.commission_schema.CommissionUpdate):
    db_commission = get_commission_by_id(db, commission_id)
    if not db_commission:
        raise HTTPException(status_code=404, detail="Commission not found")

    for key, value in commission_update.dict(exclude_unset=True).items():
        setattr(db_commission, key, value)

    db.commit()
    db.refresh(db_commission)
    return db_commission

def delete_commission(db: Session, commission_id: int):
    db_commission = get_commission_by_id(db, commission_id)
    if not db_commission:
        raise HTTPException(status_code=404, detail="Commission not found")

    db.delete(db_commission)
    db.commit()
