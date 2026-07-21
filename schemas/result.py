from pydantic import BaseModel
from pydantic import Field


class ResultCreate(BaseModel):

    student_id: int

    exam_id: int

    marks_obtained: int = Field(..., ge=0)

    grade: str | None = None

    result_status: str | None = None


class ResultResponse(ResultCreate):

    id: int

    class Config:
        from_attributes = True
