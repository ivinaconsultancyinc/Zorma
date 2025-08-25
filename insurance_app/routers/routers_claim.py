from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from insurance_app.database import get_db
from insurance_app.schemas.claim_schema import ClaimCreate, ClaimUpdate, ClaimOut
from insurance_app.schemas.document_schema import DocumentOut
from insurance_app.services import claim_service, document_service

router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)

@router.post("/", response_model=ClaimOut, status_code=status.HTTP_201_CREATED)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    return claim_service.create_claim(db, claim)

@router.get("/", response_model=List[ClaimOut])
def get_all_claims(db: Session = Depends(get_db)):
    return claim_service.get_all_claims(db)

@router.get("/{claim_id}", response_model=ClaimOut)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    db_claim = claim_service.get_claim_by_id(db, claim_id)
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return db_claim

@router.put("/{claim_id}", response_model=ClaimOut)
def update_claim(claim_id: int, claim_update: ClaimUpdate, db: Session = Depends(get_db)):
    return claim_service.update_claim(db, claim_id, claim_update)

@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(claim_id: int, db: Session = Depends(get_db)):
    claim_service.delete_claim(db, claim_id)

@router.get("/{claim_id}/documents", response_model=List[DocumentOut])
def get_documents_for_claim(claim_id: int, db: Session = Depends(get_db)):
    return document_service.get_documents_by_entity(db, "claim", claim_id)





