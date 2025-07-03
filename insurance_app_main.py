from fastapi import FastAPI
from insurance_app.routers import (
    client,
    policy,
    product,
    premium,
    commission,
    claim,
    customer,
    agent,
    document,
    audit,
    ledger,
    reinsurance
)
from insurance_app import views

app = FastAPI(title="Insurance Company of Africa Management System")

# Include routers for each module
app.include_router(client.router, prefix="/clients", tags=["Clients"])
app.include_router(policy.router, prefix="/policies", tags=["Policies"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(premium.router, prefix="/premiums", tags=["Premiums"])
app.include_router(commission.router, prefix="/commissions", tags=["Commissions"])
app.include_router(claim.router, prefix="/claims", tags=["Claims & Loans"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])
app.include_router(agent.router, prefix="/agents", tags=["Agents"])
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])
app.include_router(ledger.router, prefix="/ledger", tags=["Ledger"])
app.include_router(reinsurance.router, prefix="/reinsurance", tags=["Reinsurance"])

# Include views router for rendering templates
app.include_router(views.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Insurance Company of Africa API"}
