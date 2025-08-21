from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
import uuid

# Create router instance
router = APIRouter(
    prefix="/policies",
    tags=["policies"],
    responses={404: {"description": "Not found"}}
)

# Pydantic models for request/response
class PolicyBase(BaseModel):
    policy_number: str = Field(..., description="Unique policy number")
    policy_type: str = Field(..., description="Type of insurance policy")
    customer_id: str = Field(..., description="Customer identifier")
    premium_amount: float = Field(..., gt=0, description="Premium amount")
    coverage_amount: float = Field(..., gt=0, description="Coverage amount")
    start_date: date = Field(..., description="Policy start date")
    end_date: date = Field(..., description="Policy end date")
    status: str = Field(default="active", description="Policy status")

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    policy_type: Optional[str] = None
    premium_amount: Optional[float] = Field(None, gt=0)
    coverage_amount: Optional[float] = Field(None, gt=0)
    end_date: Optional[date] = None
    status: Optional[str] = None

class PolicyResponse(PolicyBase):
    id: str = Field(..., description="Unique policy ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class ClaimRequest(BaseModel):
    policy_id: str = Field(..., description="Associated policy ID")
    claim_amount: float = Field(..., gt=0, description="Claimed amount")
    incident_date: date = Field(..., description="Date of incident")
    description: str = Field(..., description="Claim description")
    claim_type: str = Field(..., description="Type of claim")

class ClaimResponse(BaseModel):
    claim_id: str = Field(..., description="Unique claim ID")
    policy_id: str = Field(..., description="Associated policy ID")
    claim_amount: float = Field(..., description="Claimed amount")
    status: str = Field(default="pending", description="Claim status")
    submitted_at: datetime = Field(..., description="Submission timestamp")
    incident_date: date = Field(..., description="Date of incident")
    description: str = Field(..., description="Claim description")

# In-memory storage (replace with database in production)
policies_db: Dict[str, Dict] = {}
claims_db: Dict[str, Dict] = {}

# Dependency for database connection (placeholder)
async def get_db():
    # In production, this would return a database connection
    return None

# Helper functions
def generate_policy_id() -> str:
    return f"POL-{uuid.uuid4().hex[:8].upper()}"

def generate_claim_id() -> str:
    return f"CLM-{uuid.uuid4().hex[:8].upper()}"

def validate_policy_exists(policy_id: str) -> Dict:
    if policy_id not in policies_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy with ID {policy_id} not found"
        )
    return policies_db[policy_id]

# Policy CRUD endpoints
@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(policy: PolicyCreate, db=Depends(get_db)):
    """
    Create a new insurance policy
    """
    policy_id = generate_policy_id()
    now = datetime.utcnow()
    
    # Validate dates
    if policy.start_date >= policy.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Policy end date must be after start date"
        )
    
    policy_data = {
        "id": policy_id,
        "policy_number": policy.policy_number,
        "policy_type": policy.policy_type,
        "customer_id": policy.customer_id,
        "premium_amount": policy.premium_amount,
        "coverage_amount": policy.coverage_amount,
        "start_date": policy.start_date,
        "end_date": policy.end_date,
        "status": policy.status,
        "created_at": now,
        "updated_at": now
    }
    
    # Check for duplicate policy number
    for existing_policy in policies_db.values():
        if existing_policy["policy_number"] == policy.policy_number:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Policy number {policy.policy_number} already exists"
            )
    
    policies_db[policy_id] = policy_data
    return PolicyResponse(**policy_data)

@router.get("/", response_model=List[PolicyResponse])
async def get_policies(
    skip: int = Query(0, ge=0, description="Number of policies to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of policies to return"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    policy_type: Optional[str] = Query(None, description="Filter by policy type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db=Depends(get_db)
):
    """
    Retrieve all policies with optional filtering
    """
    policies = list(policies_db.values())
    
    # Apply filters
    if customer_id:
        policies = [p for p in policies if p["customer_id"] == customer_id]
    if policy_type:
        policies = [p for p in policies if p["policy_type"] == policy_type]
    if status:
        policies = [p for p in policies if p["status"] == status]
    
    # Apply pagination
    policies = policies[skip:skip + limit]
    
    return [PolicyResponse(**policy) for policy in policies]

@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Retrieve a specific policy by ID
    """
    policy_data = validate_policy_exists(policy_id)
    return PolicyResponse(**policy_data)

@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_update: PolicyUpdate,
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Update an existing policy
    """
    policy_data = validate_policy_exists(policy_id)
    
    # Update only provided fields
    update_data = policy_update.dict(exclude_unset=True)
    
    # Validate end date if being updated
    if "end_date" in update_data:
        start_date = policy_data.get("start_date")
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date).date()
        if update_data["end_date"] <= start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Policy end date must be after start date"
            )
    
    # Update the policy
    for field, value in update_data.items():
        policy_data[field] = value
    
    policy_data["updated_at"] = datetime.utcnow()
    policies_db[policy_id] = policy_data
    
    return PolicyResponse(**policy_data)

@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Delete a policy (soft delete by setting status to 'cancelled')
    """
    policy_data = validate_policy_exists(policy_id)
    
    # Soft delete
    policy_data["status"] = "cancelled"
    policy_data["updated_at"] = datetime.utcnow()
    policies_db[policy_id] = policy_data

@router.post("/{policy_id}/renew", response_model=PolicyResponse)
async def renew_policy(
    policy_id: str = Path(..., description="Unique policy identifier"),
    renewal_months: int = Query(12, ge=1, le=60, description="Renewal period in months"),
    db=Depends(get_db)
):
    """
    Renew an existing policy
    """
    policy_data = validate_policy_exists(policy_id)
    
    if policy_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active policies can be renewed"
        )
    
    # Calculate new end date
    from dateutil.relativedelta import relativedelta
    current_end_date = policy_data["end_date"]
    if isinstance(current_end_date, str):
        current_end_date = datetime.fromisoformat(current_end_date).date()
    
    new_end_date = current_end_date + relativedelta(months=renewal_months)
    
    policy_data["end_date"] = new_end_date
    policy_data["updated_at"] = datetime.utcnow()
    policies_db[policy_id] = policy_data
    
    return PolicyResponse(**policy_data)

# Claims endpoints
@router.post("/{policy_id}/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_request: ClaimRequest,
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Create a new claim for a policy
    """
    policy_data = validate_policy_exists(policy_id)
    
    if policy_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Claims can only be created for active policies"
        )
    
    # Validate claim amount doesn't exceed coverage
    if claim_request.claim_amount > policy_data["coverage_amount"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Claim amount exceeds policy coverage limit of {policy_data['coverage_amount']}"
        )
    
    claim_id = generate_claim_id()
    now = datetime.utcnow()
    
    claim_data = {
        "claim_id": claim_id,
        "policy_id": policy_id,
        "claim_amount": claim_request.claim_amount,
        "status": "pending",
        "submitted_at": now,
        "incident_date": claim_request.incident_date,
        "description": claim_request.description,
        "claim_type": claim_request.claim_type
    }
    
    claims_db[claim_id] = claim_data
    return ClaimResponse(**claim_data)

@router.get("/{policy_id}/claims", response_model=List[ClaimResponse])
async def get_policy_claims(
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Retrieve all claims for a specific policy
    """
    validate_policy_exists(policy_id)
    
    policy_claims = [
        claim for claim in claims_db.values() 
        if claim["policy_id"] == policy_id
    ]
    
    return [ClaimResponse(**claim) for claim in policy_claims]

@router.get("/{policy_id}/summary")
async def get_policy_summary(
    policy_id: str = Path(..., description="Unique policy identifier"),
    db=Depends(get_db)
):
    """
    Get a summary of policy information including claims
    """
    policy_data = validate_policy_exists(policy_id)
    
    # Get policy claims
    policy_claims = [
        claim for claim in claims_db.values() 
        if claim["policy_id"] == policy_id
    ]
    
    total_claims = len(policy_claims)
    total_claimed_amount = sum(claim["claim_amount"] for claim in policy_claims)
    pending_claims = len([c for c in policy_claims if c["status"] == "pending"])
    approved_claims = len([c for c in policy_claims if c["status"] == "approved"])
    
    return {
        "policy": PolicyResponse(**policy_data),
        "claims_summary": {
            "total_claims": total_claims,
            "total_claimed_amount": total_claimed_amount,
            "pending_claims": pending_claims,
            "approved_claims": approved_claims
        },
        "utilization_rate": (total_claimed_amount / policy_data["coverage_amount"]) * 100
    }

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check endpoint for the policies service
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "total_policies": len(policies_db),
        "total_claims": len(claims_db)
    }
