from sqlalchemy.orm import Session
from insurance_app.models.policy import Policy
from insurance_app.schemas.policy_schema import PolicyCreate, PolicyUpdate
import uuid

class PolicyService:
    def __init__(self, db: Session):
        self.db = db

    def create_policy(self, policy_data: PolicyCreate) -> Policy:
        policy = Policy(
            id=uuid.uuid4(),
            client_id=policy_data.client_id,
            product_id=policy_data.product_id,
            policy_number=policy_data.policy_number,
            issue_date=policy_data.issue_date,
            status=policy_data.status,
            currency=policy_data.currency,
            sum_assured=policy_data.sum_assured,
            premium_frequency=policy_data.premium_frequency
        )
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def get_all_policies(self):
        return self.db.query(Policy).all()

    def get_policy_by_id(self, policy_id: uuid.UUID):
        return self.db.query(Policy).filter(Policy.id == policy_id).first()

    def update_policy(self, policy_id: uuid.UUID, policy_data: PolicyUpdate):
        policy = self.get_policy_by_id(policy_id)
        if not policy:
            return None
        for field, value in policy_data.dict(exclude_unset=True).items():
            setattr(policy, field, value)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def delete_policy(self, policy_id: uuid.UUID):
        policy = self.get_policy_by_id(policy_id)
        if policy:
            self.db.delete(policy)
            self.db.commit()