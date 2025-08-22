from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date
from enum import Enum

class AgentStatusEnum(str, Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"

class AgentBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    phone_number: Optional[str] = None
    hire_date: Optional[date] = None
    status: Optional[AgentStatusEnum] = AgentStatusEnum.active
    license_number: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    pass

class AgentOut(AgentBase):
    id: int

    class Config:
        orm_mode = True
