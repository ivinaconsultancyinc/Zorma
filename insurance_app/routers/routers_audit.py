from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from insurance_app.database import get_db
from schemas.audit_schema import AuditLogCreate, AuditLogResponse
from services.audit_service import create_audit_log, get_audit_logs
from typing import List

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.post("/", response_model=AuditLogResponse)
def log_action(audit_data: AuditLogCreate, db: Session = Depends(get_db)):
    return create_audit_log(db, audit_data)

@router.get("/", response_model=List[AuditLogResponse])
def list_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_audit_logs(db, skip=skip, limit=limit)


