from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete="CASCADE"))

    group = relationship('Class', back_populates='students')
    grades = relationship('Grade', back_populates='student')


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))

    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))

    subject = relationship('Subject', back_populates='grades')
    student = relationship('Student', back_populates='grades')
