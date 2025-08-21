from pydantic import BaseModel
from datetime import date
from typing import Optional

class CommissionBase(BaseModel):
    agent_id: int
    policy_id: int
    commission_date: date
    amount: float

class CommissionCreate(CommissionBase):
    pass

class CommissionUpdate(BaseModel):
    commission_date: Optional[date] = None
    amount: Optional[float] = None

class CommissionOut(CommissionBase):
    id: int

    class Config:
        orm_mode = True


