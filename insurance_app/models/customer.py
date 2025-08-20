from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from insurance_app.database import Base
import enum

class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    address = Column(String(255), nullable=True)
    national_id = Column(String(50), unique=True, nullable=True)

    # Relationships
    policies = relationship("Policy", back_populates="customer", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="customer", cascade="all, delete-orphan")
