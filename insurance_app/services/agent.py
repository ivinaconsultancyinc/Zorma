from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from insurance_app import models, schemas

def create_agent(db: Session, agent: schemas.AgentCreate):
    db_agent = models.Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_all_agents(db: Session):
    return db.query(models.Agent).all()

def get_agent_by_id(db: Session, agent_id: int):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent

def update_agent(db: Session, agent_id: int, agent_data: schemas.AgentUpdate):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
   
    for key, value in agent_data.dict(exclude_unset=True).items():
        setattr(agent, key, value)
   
    db.commit()
    db.refresh(agent)
    return agent

def delete_agent(db: Session, agent_id: int):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
   
    db.delete(agent)
     