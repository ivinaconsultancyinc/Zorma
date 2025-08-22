from sqlalchemy.orm import Session
from insurance_app.models.premium import Premium
from insurance_app.schemas.premium_schema import PremiumCreate, PremiumUpdate
import uuid

class PremiumService:
    def __init__(self, db: Session):
        self.db = db

    def create_premium(self, premium_data: PremiumCreate) -> Premium:
        premium = Premium(
            id=uuid.uuid4(),
            policy_id=premium_data.policy_id,
            due_date=premium_data.due_date,
            amount_due=premium_data.amount_due,
            amount_paid=premium_data.amount_paid,
            payment_date=premium_data.payment_date,
            status=premium_data.status
        )
        self.db.add(premium)
        self.db.commit()
        self.db.refresh(premium)
        return premium

    def get_all_premiums(self):
        return self.db.query(Premium).all()

    def get_premium_by_id(self, premium_id: uuid.UUID):
        return self.db.query(Premium).filter(Premium.id == premium_id).first()

    def update_premium(self, premium_id: uuid.UUID, premium_data: PremiumUpdate):
        premium = self.get_premium_by_id(premium_id)
        if not premium:
            return None
        for field, value in premium_data.dict(exclude_unset=True).items():
            setattr(premium, field, value)
        self.db.commit()
        self.db.refresh(premium)
        return premium

    def delete_premium(self, premium_id: uuid.UUID):
        premium = self.get_premium_by_id(premium_id)
        if premium:
            self.db.delete(premium)
            self.db.commit()