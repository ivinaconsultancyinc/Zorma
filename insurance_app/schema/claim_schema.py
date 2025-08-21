from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional

class ClaimStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"

class ClaimBase(BaseModel):
    policy_id: int
    claim_date: date
    claim_amount: float
    description: Optional[str] = None
    status: ClaimStatus = ClaimStatus.pending

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    claim_date: Optional[date] = None
    claim_amount: Optional[float] = None
    description: Optional[str] = None
    status: Optional[ClaimStatus] = None

class ClaimOut(ClaimBase):
    id: int

    class Config:
        orm_mode = True
