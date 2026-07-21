CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(30)
);

CREATE TABLE students(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    register_number VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    semester INTEGER
);

CREATE TABLE subjects(
    id INTEGER PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE,
    subject_name VARCHAR(100),
    faculty_name VARCHAR(100),
    credits INTEGER
);

CREATE TABLE exams(
    id INTEGER PRIMARY KEY,
    subject_id INTEGER,
    exam_name VARCHAR(100),
    exam_date DATE,
    duration INTEGER,
    total_marks INTEGER,
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
);

CREATE TABLE results(
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    exam_id INTEGER,
    marks_obtained INTEGER,
    grade VARCHAR(5),
    result_status VARCHAR(20),
    UNIQUE(student_id, exam_id),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(exam_id) REFERENCES exams(id)
);
