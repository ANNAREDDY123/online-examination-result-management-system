from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Subject(Base):

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    subject_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    subject_name = Column(String(100), nullable=False)

    faculty_name = Column(String(100), nullable=False)

    credits = Column(Integer, nullable=False)
