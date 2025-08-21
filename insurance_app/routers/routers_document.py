from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from uuid import uuid4

from insurance_app import schemas, services
from insurance_app.database import get_db

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploaded_files"

@router.post("/", response_model=schemas.document_schema.DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    related_entity: str,
    related_entity_id: int,
    uploaded_by: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_data = schemas.document_schema.DocumentCreate(
        filename=file.filename,
        file_path=file_path,
        related_entity=related_entity,
        related_entity_id=related_entity_id,
        uploaded_by=uploaded_by
    )

    return services.document_service.create_document(db, document_data)

@router.get("/", response_model=List[schemas.document_schema.DocumentOut])
def get_all_documents(db: Session = Depends(get_db)):
    return services.document_service.get_all_documents(db)

@router.get("/{document_id}", response_model=schemas.document_schema.DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = services.document_service.get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    services.document_service.delete_document(db, document_id)
