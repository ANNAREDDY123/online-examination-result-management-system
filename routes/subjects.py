from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.subject import Subject
from schemas.subject import SubjectCreate

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Subject).filter(
        Subject.subject_code == subject.subject_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Subject code already exists."
        )

    db_subject = Subject(**subject.dict())

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


@router.get("/")
def get_subjects(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    total = db.query(Subject).count()

    subjects = db.query(Subject).offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": subjects
    }


@router.get("/{subject_id}")
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found."
        )

    return subject


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):

    db_subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not db_subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found."
        )

    duplicate = db.query(Subject).filter(
        Subject.subject_code == subject.subject_code,
        Subject.id != subject_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Subject code already exists."
        )

    db_subject.subject_code = subject.subject_code
    db_subject.subject_name = subject.subject_name
    db_subject.faculty_name = subject.faculty_name
    db_subject.credits = subject.credits

    db.commit()
    db.refresh(db_subject)

    return db_subject


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found."
        )

    db.delete(subject)
    db.commit()

    return {
        "message": "Subject deleted successfully."
    }
