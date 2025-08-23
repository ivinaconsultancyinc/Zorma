from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from insurance_app.schemas.commission_schema import CommissionCreate, CommissionOut
from models_commission import Commission  # Assuming you have a SQLAlchemy model defined
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CommissionOut, status_code=status.HTTP_201_CREATED)
def create_commission(commission: CommissionCreate, db: Session = Depends(get_db)):
    new_commission = Commission(**commission.dict())
    db.add(new_commission)
    db.commit()
    db.refresh(new_commission)
    return new_commission
