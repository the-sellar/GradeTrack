from dataclasses import dataclass


@dataclass
class Grade:
    grade_id: int
    student_id: int
    subject_id: int
    value: int
    grade_date: str

