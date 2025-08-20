from sqlalchemy import Column, Date, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from insurance_app.database import Base
import uuid

class Premium(Base):
    __tablename__ = "premiums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    amount_due = Column(Numeric, nullable=False)
    amount_paid = Column(Numeric, default=0.0)
    payment_date = Column(Date, nullable=True)
    status = Column(Enum("Paid", "Unpaid", "Partial", name="premium_status_enum"), default="Unpaid")
