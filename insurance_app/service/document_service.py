from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os

from insurance_app import models, schemas

def create_document(db: Session, document: schemas.document_schema.DocumentCreate):
    db_document = models.document.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_all_documents(db: Session):
    return db.query(models.document.Document).all()

def get_document_by_id(db: Session, document_id: int):
    return db.query(models.document.Document).filter(models.document.Document.id == document_id).first()

def delete_document(db: Session, document_id: int):
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(db_document.file_path):
        os.remove(db_document.file_path)

    db.delete(db_document)
    db.commit()

# 🔗 New function to retrieve documents by related entity
def get_documents_by_entity(db: Session, entity: str, entity_id: int):
    return db.query(models.document.Document).filter(
        models.document.Document.related_entity == entity,
        models.document.Document.related_entity_id == entity_id
    ).all()


