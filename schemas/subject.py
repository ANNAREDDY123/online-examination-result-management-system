from pydantic import BaseModel
from pydantic import Field


class SubjectCreate(BaseModel):

    subject_code: str = Field(..., min_length=2, max_length=20)

    subject_name: str = Field(..., min_length=2)

    faculty_name: str = Field(..., min_length=2)

    credits: int = Field(..., gt=0)


class SubjectResponse(SubjectCreate):

    id: int

    class Config:
        from_attributes = True
