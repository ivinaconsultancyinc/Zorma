from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from insurance_app import schemas, services
from insurance_app.database import get_db

router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)

@router.post("/", response_model=schemas.claim_schema.ClaimOut, status_code=status.HTTP_201_CREATED)
def create_claim(claim: schemas.claim_schema.ClaimCreate, db: Session = Depends(get_db)):
    return services.claim_service.create_claim(db, claim)

@router.get("/", response_model=List[schemas.claim_schema.ClaimOut])
def get_all_claims(db: Session = Depends(get_db)):
    return services.claim_service.get_all_claims(db)

@router.get("/{claim_id}", response_model=schemas.claim_schema.ClaimOut)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    db_claim = services.claim_service.get_claim_by_id(db, claim_id)
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return db_claim

@router.put("/{claim_id}", response_model=schemas.claim_schema.ClaimOut)
def update_claim(claim_id: int, claim_update: schemas.claim_schema.ClaimUpdate, db: Session = Depends(get_db)):
    return services.claim_service.update_claim(db, claim_id, claim_update)

@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(claim_id: int, db: Session = Depends(get_db)):
    services.claim_service.delete_claim(db, claim_id)

# 🔗 New endpoint to fetch documents related to a claim
@router.get("/{claim_id}/documents", response_model=List[schemas.document_schema.DocumentOut])
def get_documents_for_claim(claim_id: int, db: Session = Depends(get_db)):
    return services.document_service.get_documents_by_entity(db, "claim", claim_id)

