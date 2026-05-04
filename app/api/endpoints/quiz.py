from fastapi import APIRouter
from app.schemas.quiz import QuizRequest
from app.services.quiz_service import generate_quiz_service

router = APIRouter()  # ✅ prefix хэрэггүй

@router.post("/generate-quiz")
async def generate_quiz(req: QuizRequest):
    return await generate_quiz_service(req.grade, req.subject)
