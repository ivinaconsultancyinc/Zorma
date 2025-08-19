from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/status")
async def get_status():
    return JSONResponse(content={"message": "Insurance App is running successfully."})

@router.get("/about")
async def get_about():
    return JSONResponse(content={"message": "This is the Insurance App, designed to manage client policies and claims."})

@router.get("/contact")
async def get_contact():
    return JSONResponse(content={"message": "Contact us at support@insuranceapp.com or call 1-800-INSURE."})

@router.get("/help")
async def get_help():
    return JSONResponse(content={"message": "Visit our help center at /docs or reach out to our support team for assistance."})