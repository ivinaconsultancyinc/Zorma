from sqlalchemy.orm import Session
from insurance_app.models.client import Client
from insurance_app.schemas.client_schema import ClientCreate, ClientUpdate
import uuid

class ClientService:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, client_data: ClientCreate) -> Client:
        client = Client(
            id=uuid.uuid4(),
            name=client_data.name,
            client_type=client_data.client_type,
            contact_info=client_data.contact_info,
            kyc_documents=client_data.kyc_documents,
            status=client_data.status
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_all_clients(self):
        return self.db.query(Client).all()

    def get_client_by_id(self, client_id: uuid.UUID):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def update_client(self, client_id: uuid.UUID, client_data: ClientUpdate):
        client = self.get_client_by_id(client_id)
        if not client:
            return None
        for field, value in client_data.dict(exclude_unset=True).items():
            setattr(client, field, value)
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete_client(self, client_id: uuid.UUID):
        client = self.get_client_by_id(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()



