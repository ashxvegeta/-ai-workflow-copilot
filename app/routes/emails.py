from fastapi import APIRouter
from app.services.email_service import get_sample_emails

router = APIRouter()

@router.get("/sample")
def fetch_sample_emails():
    return get_sample_emails()
