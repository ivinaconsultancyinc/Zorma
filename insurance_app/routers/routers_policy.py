from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from insurance_app.schemas.policy_schema import PolicyCreate, PolicyResponse
from insurance_app.models.policy import Policy
from insurance_app.database import SessionLocal
router = APIRouter()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    new_policy = Policy(**policy.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy
