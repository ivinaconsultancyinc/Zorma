from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Create router instance
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Enum for product types
class ProductType(str, Enum):
    LIFE = "life"
    HEALTH = "health"
    AUTO = "auto"
    HOME = "home"
    BUSINESS = "business"

# Enum for product status
class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"

# Pydantic models
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    product_type: ProductType
    base_premium: float = Field(..., gt=0)
    coverage_amount: float = Field(..., gt=0)
    deductible: Optional[float] = Field(0, ge=0)
    terms_conditions: str
    status: ProductStatus = ProductStatus.ACTIVE

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    product_type: Optional[ProductType] = None
    base_premium: Optional[float] = Field(None, gt=0)
    coverage_amount: Optional[float] = Field(None, gt=0)
    deductible: Optional[float] = Field(None, ge=0)
    terms_conditions: Optional[str] = None
    status: Optional[ProductStatus] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Mock database (replace with actual database in production)
fake_products_db = [
    {
        "id": 1,
        "name": "Comprehensive Life Insurance",
        "description": "Complete life insurance coverage with flexible premium options",
        "product_type": "life",
        "base_premium": 150.00,
        "coverage_amount": 100000.00,
        "deductible": 0.00,
        "terms_conditions": "Standard terms apply with 30-day grace period",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "name": "Premium Health Insurance",
        "description": "Comprehensive health coverage including dental and vision",
        "product_type": "health",
        "base_premium": 300.00,
        "coverage_amount": 50000.00,
        "deductible": 500.00,
        "terms_conditions": "Network providers required for full coverage",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 3,
        "name": "Auto Protection Plus",
        "description": "Full coverage auto insurance with roadside assistance",
        "product_type": "auto",
        "base_premium": 120.00,
        "coverage_amount": 25000.00,
        "deductible": 250.00,
        "terms_conditions": "Valid driver's license required",
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Helper function to get next ID
def get_next_id():
    return max([p["id"] for p in fake_products_db], default=0) + 1

# Helper function to find product by ID
def find_product_by_id(product_id: int):
    return next((product for product in fake_products_db if product["id"] == product_id), None)

# Routes
@router.get("/", response_model=List[Product])
async def get_all_products(
    product_type: Optional[ProductType] = None,
    status: Optional[ProductStatus] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all insurance products with optional filtering
    """
    products = fake_products_db.copy()
    
    # Filter by product type if specified
    if product_type:
        products = [p for p in products if p["product_type"] == product_type]
    
    # Filter by status if specified
    if status:
        products = [p for p in products if p["status"] == status]
    
    # Apply pagination
    return products[skip:skip + limit]

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """
    Retrieve a specific insurance product by ID
    """
    product = find_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new insurance product
    """
    # Check if product with same name already exists
    existing_product = next((p for p in fake_products_db if p["name"] == product.name), None)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name '{product.name}' already exists"
        )
    
    # Create new product
    new_product = {
        "id": get_next_id(),
        **product.dict(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    fake_products_db.append(new_product)
    return new_product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductUpdate):
    """
    Update an existing insurance product
    """
    product = find_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    # Update only provided fields
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        product[field] = value
    
    product["updated_at"] = datetime.now()
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    """
    Delete an insurance product
    """
    product = find_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    fake_products_db.remove(product)
    return None

@router.get("/type/{product_type}", response_model=List[Product])
async def get_products_by_type(product_type: ProductType):
    """
    Retrieve all products of a specific type
    """
    products = [p for p in fake_products_db if p["product_type"] == product_type]
    return products

@router.patch("/{product_id}/status", response_model=Product)
async def update_product_status(product_id: int, new_status: ProductStatus):
    """
    Update only the status of a specific product
    """
    product = find_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    product["status"] = new_status
    product["updated_at"] = datetime.now()
    return product

@router.get("/search/{search_term}", response_model=List[Product])
async def search_products(search_term: str):
    """
    Search products by name or description
    """
    search_term = search_term.lower()
    matching_products = [
        p for p in fake_products_db 
        if search_term in p["name"].lower() or search_term in p["description"].lower()
    ]
    return matching_products
