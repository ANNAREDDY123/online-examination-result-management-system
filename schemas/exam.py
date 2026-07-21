from datetime import date

from pydantic import BaseModel
from pydantic import Field


class ExamCreate(BaseModel):

    subject_id: int

    exam_name: str = Field(..., min_length=2)

    exam_date: date

    duration: int = Field(..., gt=0)

    total_marks: int = Field(..., gt=0)


class ExamResponse(ExamCreate):

    id: int

    class Config:
        from_attributes = True
