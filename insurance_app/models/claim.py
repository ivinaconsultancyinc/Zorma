from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from insurance_app.database import Base
import enum

class ClaimStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    claim_date = Column(Date, nullable=False)
    claim_amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.PENDING)

    # Relationships
    policy = relationship("Policy", back_populates="claims")

