from datetime import date


def valid_exam_date(exam_date):

    return exam_date >= date.today()


def valid_marks(
    marks_obtained,
    total_marks
):

    return 0 <= marks_obtained <= total_marks


def calculate_grade(
    marks_obtained,
    total_marks
):

    percentage = (marks_obtained / total_marks) * 100

    if percentage >= 90:
        return "O"

    if percentage >= 80:
        return "A+"

    if percentage >= 70:
        return "A"

    if percentage >= 60:
        return "B"

    if percentage >= 50:
        return "C"

    if percentage >= 40:
        return "D"

    return "F"


def calculate_result_status(
    marks_obtained,
    total_marks
):

    if marks_obtained == 0:
        return "Absent"

    percentage = (marks_obtained / total_marks) * 100

    if percentage >= 40:
        return "Pass"

    return "Fail"
