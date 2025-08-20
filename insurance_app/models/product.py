from sqlalchemy import Column, String, Enum, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from insurance_app.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum("Life", "Non-Life", "Group Life", "Group Medical", name="product_type_enum"), nullable=False)
    description = Column(Text, nullable=True)
    rate_table = Column(JSON, nullable=True)  # JSON structure for premium calculation
    status = Column(Enum("Active", "Inactive", name="product_status_enum"), default="Active")

