from fastapi import FastAPI
from insurance_app.routers import (
    routers_client,
    routers_policy,
    routers_product,
    routers_premium,
    routers_commission,
    routers_claim,
    routers_customer,
    routers_agent,
    routers_document,
    routers_audit,
    routers_ledger,
    routers_reinsurance
)
from insurance_app import views

app = FastAPI(title="Insurance Company of Africa Management System")

# Include routers for each module
app.include_router(routers_client.router, prefix="/clients", tags=["Clients"])
app.include_router(routers_policy.router, prefix="/policies", tags=["Policies"])
app.include_router(routers_product.router, prefix="/products", tags=["Products"])
app.include_router(routers_premium.router, prefix="/premiums", tags=["Premiums"])
app.include_router(routers_commission.router, prefix="/commissions", tags=["Commissions"])
app.include_router(routers_claim.router, prefix="/claims", tags=["Claims & Loans"])
app.include_router(routers_customer.router, prefix="/customers", tags=["Customers"])
app.include_router(routers_agent.router, prefix="/agents", tags=["Agents"])
app.include_router(routers_document.router, prefix="/documents", tags=["Documents"])
app.include_router(routers_audit.router, prefix="/audit", tags=["Audit"])
app.include_router(routers_ledger.router, prefix="/ledger", tags=["Ledger"])
app.include_router(routers_reinsurance.router, prefix="/reinsurance", tags=["Reinsurance"])

# Include views router for rendering templates
app.include_router(views.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Insurance Company of Africa API"}
