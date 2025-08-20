from sqlalchemy import Column, String, Enum, Date, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from insurance_app.database import Base
import uuid

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    policy_number = Column(String, unique=True, nullable=False)
    issue_date = Column(Date, nullable=False)
    status = Column(Enum("Active", "Lapsed", "Cancelled", name="policy_status_enum"), default="Active")
    currency = Column(String(3), nullable=False)  # e.g., USD or LRD
    sum_assured = Column(Numeric, nullable=False)
    premium_frequency = Column(Enum("Monthly", "Quarterly", "Annually", name="premium_frequency_enum"), nullable=False)
