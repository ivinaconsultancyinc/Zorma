from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/form/{module_name}", response_class=HTMLResponse)
async def render_form(request: Request, module_name: str):
    valid_templates = [
        "clients", "policies", "products", "premiums", "commissions",
        "claims", "customers", "agents", "documents", "audit", "ledger", "reinsurance"
    ]
    if module_name not in valid_templates:
        return HTMLResponse(content="Form not found", status_code=404)
    return templates.TemplateResponse(f"{module_name}.html", {"request": request})




