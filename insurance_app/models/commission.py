from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from insurance_app.database import Base

class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    commission_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

    # Relationships
    agent = relationship("Agent", back_populates="commissions")
    policy = relationship("Policy", back_populates="commissions")

