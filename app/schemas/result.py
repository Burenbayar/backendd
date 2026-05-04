from pydantic import BaseModel
from datetime import datetime

class QuizResultIn(BaseModel):
    grade: int | None = None
    subject: str
    score: int
    total: int
    percentage: float
    duration_seconds: int | None = None

class QuizResultOut(BaseModel):
    id: int
    subject: str
    grade: int | None = None
    score: int
    total: int
    percentage: float
    duration_seconds: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True
