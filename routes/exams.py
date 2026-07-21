from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.exam import Exam
from models.subject import Subject
from schemas.exam import ExamCreate
from services.result_service import valid_exam_date

router = APIRouter(
    prefix="/exams",
    tags=["Examinations"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_exam(
    exam: ExamCreate,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == exam.subject_id
    ).first()

    if not subject:

        raise HTTPException(
            status_code=404,
            detail="Subject not found."
        )

    if not valid_exam_date(exam.exam_date):

        raise HTTPException(
            status_code=400,
            detail="Exam date cannot be in the past."
        )

    db_exam = Exam(**exam.dict())

    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)

    return db_exam


@router.get("/")
def get_exams(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    total = db.query(Exam).count()

    exams = db.query(Exam).offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": exams
    }


@router.get("/{exam_id}")
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db)
):

    exam = db.query(Exam).filter(
        Exam.id == exam_id
    ).first()

    if not exam:

        raise HTTPException(
            status_code=404,
            detail="Exam not found."
        )

    return exam


@router.put("/{exam_id}")
def update_exam(
    exam_id: int,
    exam: ExamCreate,
    db: Session = Depends(get_db)
):

    db_exam = db.query(Exam).filter(
        Exam.id == exam_id
    ).first()

    if not db_exam:

        raise HTTPException(
            status_code=404,
            detail="Exam not found."
        )

    if not valid_exam_date(exam.exam_date):

        raise HTTPException(
            status_code=400,
            detail="Exam date cannot be in the past."
        )

    db_exam.subject_id = exam.subject_id
    db_exam.exam_name = exam.exam_name
    db_exam.exam_date = exam.exam_date
    db_exam.duration = exam.duration
    db_exam.total_marks = exam.total_marks

    db.commit()
    db.refresh(db_exam)

    return db_exam


@router.delete("/{exam_id}")
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db)
):

    exam = db.query(Exam).filter(
        Exam.id == exam_id
    ).first()

    if not exam:

        raise HTTPException(
            status_code=404,
            detail="Exam not found."
        )

    db.delete(exam)
    db.commit()

    return {
        "message": "Exam deleted successfully."
    }
