from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from insurance_app import models, schemas

def create_claim(db: Session, claim: schemas.claim_schema.ClaimCreate):
    db_claim = models.claim.Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

def get_all_claims(db: Session):
    return db.query(models.claim.Claim).all()

def get_claim_by_id(db: Session, claim_id: int):
    return db.query(models.claim.Claim).filter(models.claim.Claim.id == claim_id).first()

def update_claim(db: Session, claim_id: int, claim_update: schemas.claim_schema.ClaimUpdate):
    db_claim = get_claim_by_id(db, claim_id)
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    for key, value in claim_update.dict(exclude_unset=True).items():
        setattr(db_claim, key, value)

    db.commit()
    db.refresh(db_claim)
    return db_claim

def delete_claim(db: Session, claim_id: int):
    db_claim = get_claim_by_id(db, claim_id)
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    db.delete(db_claim)
    db.commit()



