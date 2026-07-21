from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Exam(Base):

    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    exam_name = Column(String(100), nullable=False)

    exam_date = Column(Date, nullable=False)

    duration = Column(Integer, nullable=False)

    total_marks = Column(Integer, nullable=False)
