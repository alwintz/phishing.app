from fastapi import APIRouter
from pydantic import BaseModel

from services.analysis_service import analyze_email

router = APIRouter()


class EmailRequest(BaseModel):
    email_text: str


@router.post("/analyze")
def analyze(request: EmailRequest):
    return analyze_email(request.email_text)