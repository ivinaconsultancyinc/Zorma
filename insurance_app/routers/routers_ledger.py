from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.ledger_schema import LedgerEntryCreate, LedgerEntryResponse
from services.ledger_service import create_ledger_entry, get_ledger_entries
from typing import List

router = APIRouter(prefix="/ledger", tags=["Ledger"])

@router.post("/", response_model=LedgerEntryResponse)
def add_entry(entry_data: LedgerEntryCreate, db: Session = Depends(get_db)):
    return create_ledger_entry(db, entry_data)

@router.get("/", response_model=List[LedgerEntryResponse])
def list_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_ledger_entries(db, skip=skip, limit=limit)


