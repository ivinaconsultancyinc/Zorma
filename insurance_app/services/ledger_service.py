from sqlalchemy.orm import Session
from models.ledger import LedgerEntry
from schemas.ledger_schema import LedgerEntryCreate

def create_ledger_entry(db: Session, entry_data: LedgerEntryCreate) -> LedgerEntry:
    entry = LedgerEntry(**entry_data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_ledger_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LedgerEntry).offset(skip).limit(limit).all()
