from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from insurance_app.database import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    related_entity = Column(String, nullable=True)  # e.g., "policy", "claim", "customer"
    related_entity_id = Column(Integer, nullable=True)

    # Relationships
    uploader = relationship("User", back_populates="documents", lazy="joined")
