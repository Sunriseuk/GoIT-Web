import sys
import os
from datetime import datetime
from random import randint

from faker import Faker

sys.path.append(os.getcwd())
from db.connect_db import session
from db.models import Teacher, Student, Subject, Class, Grade

fake_data = Faker()

NUMBER_CLASSES = 3
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 10 * NUMBER_STUDENTS


def create_classes():
    for class_name in ["The Immortals",
                       "The Shrewd Shrews", "The Sleepy Scholars"]:
        class_ = Class(
            name=class_name
        )
        session.add(class_)
    session.commit()


def create_students():
    for _ in range(NUMBER_STUDENTS):
        student = Student(
            fullname=fake_data.name(),
            class_id=randint(1, NUMBER_CLASSES)
        )
        session.add(student)
    session.commit()


def create_teachers():
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(
            fullname=fake_data.name(),
        )
        session.add(teacher)
    session.commit()


def create_subjects():
    for subject_name in ["English", "Math", "Art", "History",
                         "Music", "Geography", "Chemistry", "Graphic design"]:
        subject = Subject(
            name=subject_name,
            teacher_id=randint(1, NUMBER_TEACHERS)
        )
        session.add(subject)
    session.commit()


def create_grades():
    for _ in range(NUMBER_GRADES):
        grade = Grade(
            grade=randint(60, 100),
            date_of=fake_data.date_between_dates(date_start=datetime(2022, 9, 1), date_end=datetime(2023, 1, 1)),
            student_id=randint(1, NUMBER_STUDENTS),
            subject_id=randint(1, NUMBER_SUBJECTS)
        )
        session.add(grade)
    session.commit()


if __name__ == '__main__':
    create_classes()
    create_students()
    create_teachers()
    create_subjects()
    create_grades()
