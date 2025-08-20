from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    entry_type = Column(String(10), nullable=False)  # e.g., 'debit' or 'credit'
    timestamp = Column(DateTime, default=datetime.utcnow)
