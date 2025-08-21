from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from insurance_app import models, schemas
from insurance_app.database import get_db
from insurance_app.services import agent_service

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

@router.post("/", response_model=schemas.AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    return agent_service.create_agent(db, agent)

@router.get("/", response_model=List[schemas.AgentOut])
def get_all_agents(db: Session = Depends(get_db)):
    return agent_service.get_all_agents(db)

@router.get("/{agent_id}", response_model=schemas.AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    return agent_service.get_agent_by_id(db, agent_id)

@router.put("/{agent_id}", response_model=schemas.AgentOut)
def update_agent(agent_id: int, agent: schemas.AgentUpdate, db: Session = Depends(get_db)):
    return agent_service.update_agent(db, agent_id, agent)

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent_service.delete_agent(db, agent_id)
    return None