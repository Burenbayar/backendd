from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.db.session import Base

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    subject = Column(String, nullable=False)
    grade = Column(Integer, nullable=True)

    score = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
