from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class StudentCreate(BaseModel):

    name: str = Field(..., min_length=2, max_length=100)

    email: EmailStr

    register_number: str = Field(..., min_length=3, max_length=30)

    department: str = Field(..., min_length=2)

    semester: int = Field(..., ge=1, le=8)


class StudentResponse(StudentCreate):

    id: int

    class Config:
        from_attributes = True
