from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from insurance_app.schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse
from insurance_app.services.client_service import ClientService
from insurance_app.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.create_client(client)

@router.get("/", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.get_all_clients()

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ClientService(db)
    client = service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: uuid.UUID, client_data: ClientUpdate, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.update_client(client_id, client_data)

@router.delete("/{client_id}")
def delete_client(client_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ClientService(db)
    service.delete_client(client_id)
    return {"message": "Client deleted successfully"}
