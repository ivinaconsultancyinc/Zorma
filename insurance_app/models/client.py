from sqlalchemy import Column, String, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from insurance_app.database import Base
import uuid

class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    client_type = Column(Enum("Individual", "Corporate", name="client_type_enum"), nullable=False)
    contact_info = Column(JSON, nullable=True)
    kyc_documents = Column(JSON, nullable=True)
    status = Column(Enum("Active", "Inactive", "Blocked", name="client_status_enum"), default="Active")