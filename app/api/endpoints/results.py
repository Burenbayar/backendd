from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.result import QuizResultIn, QuizResultOut
from app.services.result_service import save_result_service
from app.services.auth_dependency import get_current_user
from app.models.user import User

router = APIRouter(prefix="/results", tags=["results"])

@router.post("", response_model=QuizResultOut)
def save_result(
    result_in: QuizResultIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return save_result_service(db, current_user.id, result_in)
