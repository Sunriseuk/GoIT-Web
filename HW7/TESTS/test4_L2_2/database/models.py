from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Date

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column('cell_phone', String(50), nullable=False)
    address = Column(String(150), nullable=True)
    start_work = Column(Date, nullable=True)
    created_at = Column(DateTime, default=func.now())

    students = relationship("Student", secondary='teachers_to_students', back_populates="teachers", passive_deletes=True)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column('cell_phone', String(150), nullable=False)
    address = Column(String(150), nullable=True)

    teachers = relationship("Teacher", secondary='teachers_to_students', back_populates="students",
                            passive_deletes=True)


class TeacherStudent(Base):
    __tablename__ = "teachers_to_students"
    id = Column(Integer, primary_key=True)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    student_id = Column('student_id', ForeignKey('students_id.id', ondelete='CASCADE'))