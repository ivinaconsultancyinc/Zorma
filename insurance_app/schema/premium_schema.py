from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class PremiumBase(BaseModel):
    policy_id: uuid.UUID
    due_date: date
    amount_due: float
    amount_paid: Optional[float] = 0.0
    payment_date: Optional[date] = None
    status: Optional[str] = "Unpaid"

class PremiumCreate(PremiumBase):
    pass

class PremiumUpdate(BaseModel):
    amount_paid: Optional[float]
    payment_date: Optional[date]
    status: Optional[str]

class PremiumResponse(PremiumBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
