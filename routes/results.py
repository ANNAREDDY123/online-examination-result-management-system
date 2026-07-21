from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.exam import Exam
from models.result import Result
from models.student import Student

from schemas.result import ResultCreate

from services.result_service import (
    valid_marks,
    calculate_grade,
    calculate_result_status
)

router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_result(
    result: ResultCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == result.student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    exam = db.query(Exam).filter(
        Exam.id == result.exam_id
    ).first()

    if not exam:

        raise HTTPException(
            status_code=404,
            detail="Exam not found."
        )

    duplicate = db.query(Result).filter(
        Result.student_id == result.student_id,
        Result.exam_id == result.exam_id
    ).first()

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Result already exists for this student and exam."
        )

    if not valid_marks(
        result.marks_obtained,
        exam.total_marks
    ):

        raise HTTPException(
            status_code=400,
            detail="Marks should be between 0 and total marks."
        )

    grade = calculate_grade(
        result.marks_obtained,
        exam.total_marks
    )

    status = calculate_result_status(
        result.marks_obtained,
        exam.total_marks
    )

    db_result = Result(
        student_id=result.student_id,
        exam_id=result.exam_id,
        marks_obtained=result.marks_obtained,
        grade=grade,
        result_status=status
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result


@router.get("/")
def get_results(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    total = db.query(Result).count()

    results = db.query(Result).offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": results
    }


@router.get("/{result_id}")
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Result not found."
        )

    return result


@router.put("/{result_id}")
def update_result(
    result_id: int,
    result: ResultCreate,
    db: Session = Depends(get_db)
):

    db_result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if not db_result:

        raise HTTPException(
            status_code=404,
            detail="Result not found."
        )

    exam = db.query(Exam).filter(
        Exam.id == result.exam_id
    ).first()

    if not exam:

        raise HTTPException(
            status_code=404,
            detail="Exam not found."
        )

    if not valid_marks(
        result.marks_obtained,
        exam.total_marks
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid marks."
        )

    db_result.student_id = result.student_id
    db_result.exam_id = result.exam_id
    db_result.marks_obtained = result.marks_obtained
    db_result.grade = calculate_grade(
        result.marks_obtained,
        exam.total_marks
    )
    db_result.result_status = calculate_result_status(
        result.marks_obtained,
        exam.total_marks
    )

    db.commit()
    db.refresh(db_result)

    return db_result


@router.get("/students/{student_id}/results")
def student_results(
    student_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Result).filter(
        Result.student_id == student_id
    ).all()


@router.get("/reports/pass-percentage")
def pass_percentage(
    db: Session = Depends(get_db)
):

    total = db.query(Result).count()

    passed = db.query(Result).filter(
        Result.result_status == "Pass"
    ).count()

    percentage = 0

    if total > 0:
        percentage = round((passed / total) * 100, 2)

    return {
        "total_results": total,
        "passed": passed,
        "pass_percentage": percentage
    }
