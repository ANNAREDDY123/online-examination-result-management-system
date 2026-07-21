# online-examination-result-management-system
A FastAPI-based Online Examination &amp; Result Management System with JWT Authentication, Role-Based Authorization, Student Management, Subject Management, Examination Management, Result Processing, Reports, Search, Pagination, SQLAlchemy ORM, Docker Support, Logging, and Unit Testing.
# Online Examination & Result Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Student Management
- Subject Management
- Examination Management
- Result Management
- Automatic Grade Calculation
- Automatic Pass/Fail Generation
- Search & Reports
- Pagination
- SQLAlchemy ORM
- Docker Support
- Logging
- Unit Test Structure



## Installation

```bash
pip install -r requirements.txt
```

---

## Run Project


py -m uvicorn main:app --reload


Swagger:

http://127.0.0.1:8000/docs


## Environment Variables


DATABASE_URL=sqlite:///./online_exam.db
SECRET_KEY=online_exam_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

## Business Rules

- Register Number must be unique.
- Subject Code must be unique.
- One result per student per exam.
- Marks must be between 0 and total marks.
- Grade calculated automatically.
- Result status generated automatically.
- Students can appear for multiple exams.



## Docker


docker build -t online-exam-system .
docker run -p 8000:8000 online-exam-system
