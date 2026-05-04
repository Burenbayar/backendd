from pydantic import BaseModel
from app.schemas.auth import UserOut
from app.schemas.result import QuizResultOut

class ProfileData(BaseModel):
    user: UserOut
    results: list[QuizResultOut]
