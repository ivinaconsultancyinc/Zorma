from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from insurance_app.database import Base
import enum

class AgentStatusEnum(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    hire_date = Column(Date, nullable=True)
    status = Column(Enum(AgentStatusEnum), default=AgentStatusEnum.active)
    license_number = Column(String(50), unique=True, nullable=True)

    # Relationships
    policies = relationship("Policy", back_populates="agent", cascade="all, delete-orphan")
    commissions = relationship("Commission", back_populates="agent", cascade="all, delete-orphan")

