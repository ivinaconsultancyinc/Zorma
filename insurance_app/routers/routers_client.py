from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
import uuid

# Create router instance
router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class ClientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    date_of_birth: date
    address: str = Field(..., min_length=10, max_length=200)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, min_length=10, max_length=200)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    state: Optional[str] = Field(None, min_length=2, max_length=50)
    zip_code: Optional[str] = Field(None, pattern=r'^\d{5}(-\d{4})?$')

class ClientResponse(ClientBase):
    client_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class PolicySummary(BaseModel):
    policy_id: str
    policy_type: str
    policy_number: str
    status: str
    premium: float
    start_date: date
    end_date: date

class ClientWithPolicies(ClientResponse):
    policies: List[PolicySummary] = []

# In-memory storage for demo purposes
# In production, replace with database operations
clients_db = {}

# Helper functions
def get_client_by_id(client_id: str):
    """Retrieve client by ID from database"""
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

def check_email_exists(email: str, exclude_id: str = None):
    """Check if email already exists"""
    for client_id, client in clients_db.items():
        if client["email"] == email and client_id != exclude_id:
            return True
    return False

# Client endpoints
@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(client: ClientCreate):
    """Create a new client"""
    # Check if email already exists
    if check_email_exists(client.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate client ID
    client_id = str(uuid.uuid4())
    
    # Create client record
    now = datetime.utcnow()
    client_data = {
        "client_id": client_id,
        "first_name": client.first_name,
        "last_name": client.last_name,
        "email": client.email,
        "phone": client.phone,
        "date_of_birth": client.date_of_birth,
        "address": client.address,
        "city": client.city,
        "state": client.state,
        "zip_code": client.zip_code,
        "created_at": now,
        "updated_at": now,
        "is_active": True
    }
    
    clients_db[client_id] = client_data
    return ClientResponse(**client_data)

@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get list of clients with optional filtering"""
    clients = list(clients_db.values())
    
    # Apply filters
    if is_active is not None:
        clients = [c for c in clients if c["is_active"] == is_active]
    
    if search:
        search_lower = search.lower()
        clients = [
            c for c in clients 
            if (search_lower in c["first_name"].lower() or 
                search_lower in c["last_name"].lower() or 
                search_lower in c["email"].lower())
        ]
    
    # Apply pagination
    total = len(clients)
    clients = clients[skip:skip + limit]
    
    return [ClientResponse(**client) for client in clients]

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: str):
    """Get client by ID"""
    client = get_client_by_id(client_id)
    return ClientResponse(**client)

@router.get("/{client_id}/with-policies", response_model=ClientWithPolicies)
async def get_client_with_policies(client_id: str):
    """Get client with their policies"""
    client = get_client_by_id(client_id)
    
    # Mock policy data - replace with actual database query
    mock_policies = [
        {
            "policy_id": str(uuid.uuid4()),
            "policy_type": "Auto Insurance",
            "policy_number": "AUTO-2024-001",
            "status": "Active",
            "premium": 1200.00,
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31)
        },
        {
            "policy_id": str(uuid.uuid4()),
            "policy_type": "Home Insurance",
            "policy_number": "HOME-2024-002",
            "status": "Active",
            "premium": 800.00,
            "start_date": date(2024, 3, 1),
            "end_date": date(2025, 2, 28)
        }
    ]
    
    client_with_policies = ClientWithPolicies(
        **client,
        policies=[PolicySummary(**policy) for policy in mock_policies]
    )
    
    return client_with_policies

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(client_id: str, client_update: ClientUpdate):
    """Update client information"""
    client = get_client_by_id(client_id)
    
    # Check email uniqueness if email is being updated
    if client_update.email and client_update.email != client["email"]:
        if check_email_exists(client_update.email, client_id):
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update fields
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        client[field] = value
    
    client["updated_at"] = datetime.utcnow()
    clients_db[client_id] = client
    
    return ClientResponse(**client)

@router.patch("/{client_id}/status", response_model=ClientResponse)
async def toggle_client_status(client_id: str):
    """Toggle client active/inactive status"""
    client = get_client_by_id(client_id)
    
    client["is_active"] = not client["is_active"]
    client["updated_at"] = datetime.utcnow()
    clients_db[client_id] = client
    
    return ClientResponse(**client)

@router.delete("/{client_id}", status_code=204)
async def delete_client(client_id: str):
    """Delete client (soft delete by setting is_active to False)"""
    client = get_client_by_id(client_id)
    
    # Soft delete
    client["is_active"] = False
    client["updated_at"] = datetime.utcnow()
    clients_db[client_id] = client
    
    # For hard delete, use: del clients_db[client_id]
    return None

@router.get("/{client_id}/policies", response_model=List[PolicySummary])
async def get_client_policies(client_id: str):
    """Get all policies for a specific client"""
    client = get_client_by_id(client_id)
    
    # Mock policy data - replace with actual database query
    mock_policies = [
        {
            "policy_id": str(uuid.uuid4()),
            "policy_type": "Auto Insurance",
            "policy_number": "AUTO-2024-001",
            "status": "Active",
            "premium": 1200.00,
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31)
        }
    ]
    
    return [PolicySummary(**policy) for policy in mock_policies]

# Health check endpoint
@router.get("/health/check")
async def health_check():
    """Health check endpoint for client router"""
    return {
        "status": "healthy",
        "service": "client_router",
        "timestamp": datetime.utcnow(),
        "total_clients": len(clients_db)
    }
