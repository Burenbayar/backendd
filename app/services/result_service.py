from sqlalchemy.orm import Session
from app.models.quiz_result import QuizResult

def save_result_service(db: Session, user_id: int, payload):
    qr = QuizResult(
        user_id=user_id,
        subject=payload.subject,
        grade=payload.grade,
        score=payload.score,
        total=payload.total,
        percentage=payload.percentage,
        duration_seconds=payload.duration_seconds,
    )
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return qr

def get_profile_results(db: Session, user_id: int):
    return (
        db.query(QuizResult)
        .filter(QuizResult.user_id == user_id)
        .order_by(QuizResult.created_at.desc())
        .all()
    )
