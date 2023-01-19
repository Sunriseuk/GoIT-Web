import sys
import os
sys.path.append(os.getcwd())

from models import Class, Student, Teacher, Subject, Grade
from connect_db import session

from sqlalchemy import func, desc, and_

def select_1():
    print('-----------------------------------------------------------------------------------------')
    q1 = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_rate')).select_from(Student).join(
        Grade).filter(Grade.student_id == Student.id).group_by(Student.id).order_by(desc('avg_rate')).limit(5).all()
    print(f'1 - 5 students with the highest GPA in all subjects is:\n{q1}')
    print('-----------------------------------------------------------------------------------------')

def select_2():
    q2 = session.query(Student.fullname, Subject.name, Grade.grade).select_from(Grade).join(Student, Subject).filter(
        and_(Student.id == Grade.student_id, Subject.id == Grade.subject_id, Subject.id == 7)).order_by(desc(Grade.grade)).limit(1).all()
    print(f'2 - The student with the highest GPA in the subject is:\n{q2}')
    print('-----------------------------------------------------------------------------------------')

def select_3():
    q3 = session.query(Class.name, func.round(func.avg(Grade.grade), 2)).select_from(Grade).join(Student, Subject,
                                                                                                       Class).filter(
            and_(Grade.student_id ==
                 Student.id, Subject.id == Grade.subject_id, Class.id == Student.class_id, Subject.id == 2)).group_by(
            Class.name).order_by(Class.name).all()
    print(f'3 - Average score in groups in the subject is:\n{q3}')
    print('-----------------------------------------------------------------------------------------')

def select_4():
    q4 = session.query(func.round(func.avg(Grade.grade), 2)).select_from(Grade).all()
    print(f'4 - Average score on the stream (for the entire rating table) is:\n{q4}')
    print('-----------------------------------------------------------------------------------------')

def select_5():
    q5 = session.query(Teacher.fullname, Subject.name).select_from(Subject).join(Teacher).filter(
            Subject.teacher_id == Teacher.id).order_by(Teacher.fullname).all()
    print(f'5 - Teacher teaches courses:\n{q5}')
    print('-----------------------------------------------------------------------------------------')

def select_6():
    q6 = session.query(Class.name, Student.fullname).select_from(Student).join(Class).filter(
            and_(Student.class_id == Class.id, Class.id == 1)).order_by(
            Student.fullname).all()
    print(f'6 - List of students:\n{q6}')
    print('-----------------------------------------------------------------------------------------')

def select_7():
    q7 = session.query(Class.name, Student.fullname, Subject.name, Grade.grade).select_from(Grade).join(Student,
                                                                                                              Class,
                                                                                                              Subject).filter(
            and_(Student.class_id == Class.id,
                 Student.id == Grade.student_id, Subject.id == Grade.subject_id)).filter(Class.id == 3).filter(
            Subject.id == 4).order_by(desc(Grade.grade)).all()
    print(f'7 - Student grades in the subject group:\n{q7}')
    print('-----------------------------------------------------------------------------------------')

def select_8():
    q8 = session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade'),
        Teacher.fullname).select_from(Grade).join(Subject).join(Teacher).group_by(Teacher.fullname).filter(
        Subject.teacher_id == Teacher.id).all()
    print(f'8 - The average score that the teacher puts in his subjects:\n{q8}')
    print('-----------------------------------------------------------------------------------------')

def select_9():
    q9 = session.query(Student.fullname, Subject.name).select_from(Student).join(Grade).join(Subject).filter(
        Student.id == 1).all()
    print(f'9 - Student attends courses:\n{q9}')
    print('-----------------------------------------------------------------------------------------')

def select_10():
    q10 =  session.query(Student.fullname, Teacher.fullname, Subject.name).select_from(Grade).join(Subject, Student,
                                                                                                       Teacher).filter(
            and_(Subject.id == Grade.subject_id,
                 Student.id == Grade.student_id, Teacher.id == Subject.teacher_id, Student.id == 10,
                 Teacher.id == 2)).order_by(Subject.name).all()
    print(f'10 - List of courses that the teacher reads to the student:\n{q10}')
    print('-----------------------------------------------------------------------------------------')

def all_select():
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()
