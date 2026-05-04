from pydantic import BaseModel

class QuizRequest(BaseModel):
    grade: int
    subject: str
