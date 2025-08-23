from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class PolicyBase(BaseModel):
    client_id: uuid.UUID
    product_id: uuid.UUID
    policy_number: str
    issue_date: date
    status: Optional[str] = "Active"
    currency: str  # "USD" or "LRD"
    sum_assured: float
    premium_frequency: str  # "Monthly", "Quarterly", "Annually"

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    status: Optional[str]
    sum_assured: Optional[float]
    premium_frequency: Optional[str]

class PolicyResponse(PolicyBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
