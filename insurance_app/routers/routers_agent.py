from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from insurance_app.schemas import agent as agent_schema
from insurance_app.services import agent as agent_service
from insurance_app.database import get_db
router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)
@router.post("/", response_model=agent_schema.AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(agent: agent_schema.AgentCreate, db: Session = Depends(get_db)):
    return agent_service.create_agent(db, agent)
@router.get("/", response_model=List[agent_schema.AgentOut])
def get_all_agents(db: Session = Depends(get_db)):
    return agent_service.get_all_agents(db)
@router.get("/{agent_id}", response_model=agent_schema.AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    return agent_service.get_agent_by_id(db, agent_id)
@router.put("/{agent_id}", response_model=agent_schema.AgentOut)
def update_agent(agent_id: int, agent: agent_schema.AgentUpdate, db: Session = Depends(get_db)):
    return agent_service.update_agent(db, agent_id, agent)
@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent_service.delete_agent(db, agent_id)
    return None

