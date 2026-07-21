from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.student import Student
from schemas.student import StudentCreate

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Student).filter(
        Student.register_number == student.register_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Register number already exists."
        )

    db_student = Student(**student.dict())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@router.get("/")
def get_students(
    register_number: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Student)

    if register_number:
        query = query.filter(
            Student.register_number.contains(register_number)
        )

    total = query.count()

    students = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": students
    }


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    return student


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    db_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    duplicate = db.query(Student).filter(
        Student.register_number == student.register_number,
        Student.id != student_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Register number already exists."
        )

    db_student.name = student.name
    db_student.email = student.email
    db_student.register_number = student.register_number
    db_student.department = student.department
    db_student.semester = student.semester

    db.commit()
    db.refresh(db_student)

    return db_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully."
    }
