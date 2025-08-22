from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LedgerEntryBase(BaseModel):
    account: str
    description: Optional[str] = None
    amount: float
    entry_type: str

class LedgerEntryCreate(LedgerEntryBase):
    pass

class LedgerEntryResponse(LedgerEntryBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
