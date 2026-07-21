from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from database import Base


class Result(Base):

    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    exam_id = Column(
        Integer,
        ForeignKey("exams.id"),
        nullable=False
    )

    marks_obtained = Column(Integer, nullable=False)

    grade = Column(String(5), nullable=False)

    result_status = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "exam_id",
            name="unique_student_exam_result"
        ),
    )
