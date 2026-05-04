from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.profile import ProfileData
from app.services.auth_dependency import get_current_user
from app.services.result_service import get_profile_results
from app.models.user import User

router = APIRouter(prefix="/profile-data", )

@router.get("", response_model=ProfileData)
def profile_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = get_profile_results(db, current_user.id)
    return {"user": current_user, "results": results}


