from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class ReinsuranceContract(Base):
    __tablename__ = "reinsurance_contracts"

    id = Column(Integer, primary_key=True, index=True)
    insurer = Column(String(100), nullable=False)
    reinsurer = Column(String(100), nullable=False)
    contract_type = Column(String(50), nullable=False)
    coverage_amount = Column(Float, nullable=False)
    premium = Column(Float, nullable=False)
    effective_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
