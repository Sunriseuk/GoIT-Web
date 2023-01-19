import sys
import os
sys.path.append(os.getcwd())

from db.models import Class, Student, Teacher, Subject, Grade
from db.connect_db import session

from sqlalchemy import func, desc, and_



def query_1():
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_rate')).select_from(Student).join(
        Grade).filter(Grade.student_id == Student.id).group_by(Student.id).order_by(desc('avg_rate')).limit(5).all()

def query_2():
    return session.query(Student.fullname, Subject.name, Grade.grade).select_from(Grade).join(Student, Subject).filter(
        and_(Student.id == Grade.student_id, Subject.id == Grade.subject_id, Subject.id == 7)).order_by(desc(Grade.grade)).limit(1).all()
    
def query_3():
    return session.query(Class.name, func.round(func.avg(Grade.grade), 2)).select_from(Grade).join(Student, Subject, Class).filter(and_(Grade.student_id == 
    Student.id, Subject.id == Grade.subject_id, Class.id == Student.class_id, Subject.id == 3)).group_by(Class.name).order_by(Class.name).all()

def query_4():
    return session.query(func.round(func.avg(Grade.grade), 2)).select_from(Grade).all()

def query_5():
    return session.query(Teacher.fullname, Subject.name).select_from(Subject).join(Teacher).filter(Subject.teacher_id == Teacher.id).order_by(Teacher.fullname).all()

def query_6():
    return session.query(Class.name, Student.fullname).select_from(Student).join(Class).filter(and_(Student.class_id == Class.id, Class.id == 1)).order_by(
        Student.fullname).all()

def query_7():
    return session.query(Class.name, Student.fullname, Subject.name, Grade.grade).select_from(Grade).join(Student, Class, Subject).filter(and_(Student.class_id == Class.id,
     Student.id == Grade.student_id, Subject.id == Grade.subject_id)).filter(Class.id == 3).filter(Subject.id == 4).order_by(desc(Grade.grade)).all()

def query_8(): # some problems
    return session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2)).select_from(Grade).join(Teacher, Subject).filter(and_(
        Teacher.id == Subject.teacher_id, Grade.subject_id == Subject.id, Teacher.id == 5)).group_by(Subject.name).all()

def query_9(): # .distinct()
    return session.query(Student.fullname, Subject.name).select_from(Student).join(Grade, Subject).filter(and_(Student.id == Grade.student_id, 
    Subject.id == Grade.subject_id, Student.id == 50)).order_by(Subject.name)
    

def query_10():
    return session.query(Student.fullname, Teacher.fullname, Subject.name).select_from(Grade).join(Subject, Student, Teacher).filter(and_(Subject.id == Grade.subject_id,
     Student.id == Grade.student_id, Teacher.id == Subject.teacher_id, Student.id == 42, Teacher.id == 3)).order_by(Subject.name).all()

def query_11():
    return session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2)).select_from(Grade).join(Subject, Student, Teacher).filter(and_(
        Subject.id == Grade.subject_id, Student.id == Grade.student_id, Teacher.id == Subject.teacher_id, Student.id == 2, Teacher.id == 2)).group_by(Teacher.fullname, Student.fullname).all()

def query_12():
    subq = session.query(func.max(Grade.date_of)).select_from(Grade).join(Student, Class, Subject).filter(and_(Grade.student_id == Student.id,
     Student.class_id == Class.id, Subject.id == Grade.subject_id, Class.id == 2, Subject.id == 1)).one()

    return session.query(Class.name, Student.fullname, Subject.name, Grade.grade, Grade.date_of).select_from(Grade, Student, Class, Subject).filter(and_(Grade.student_id == Student.id,
     Student.class_id == Class.id, Subject.id == Grade.subject_id, Class.id == 2, Subject.id == 1, Grade.date_of.in_(subq))).all()

for r in query_12():
    print(r)