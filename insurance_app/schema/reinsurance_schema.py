from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReinsuranceContractBase(BaseModel):
    insurer: str
    reinsurer: str
    contract_type: str
    coverage_amount: float
    premium: float
    effective_date: datetime
    expiration_date: datetime

class ReinsuranceContractCreate(ReinsuranceContractBase):
    pass

class ReinsuranceContractResponse(ReinsuranceContractBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
