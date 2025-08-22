from pydantic import BaseModel
from typing import Optional, Dict
import uuid

class ProductBase(BaseModel):
    name: str
    type: str  # "Life", "Non-Life", "Group Life", "Group Medical"
    description: Optional[str] = None
    rate_table: Optional[Dict] = None
    status: Optional[str] = "Active"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str]
    rate_table: Optional[Dict]
    status: Optional[str]

class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

