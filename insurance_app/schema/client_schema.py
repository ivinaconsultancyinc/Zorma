from pydantic import BaseModel
from typing import Optional, Dict
import uuid

class ClientBase(BaseModel):
    name: str
    client_type: str  # "Individual" or "Corporate"
    contact_info: Optional[Dict] = None
    kyc_documents: Optional[Dict] = None
    status: Optional[str] = "Active"

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: uuid.UUID

    class Config:
        from_attributes = True