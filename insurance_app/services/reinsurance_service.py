from sqlalchemy.orm import Session
from models.reinsurance import ReinsuranceContract
from schemas.reinsurance_schema import ReinsuranceContractCreate

def create_contract(db: Session, contract_data: ReinsuranceContractCreate) -> ReinsuranceContract:
    contract = ReinsuranceContract(**contract_data.dict())
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def get_contracts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReinsuranceContract).offset(skip).limit(limit).all()







