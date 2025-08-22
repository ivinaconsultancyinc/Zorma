from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class CustomerBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = None
    national_id: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True
