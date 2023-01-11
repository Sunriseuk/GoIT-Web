from datetime import datetime
import faker
from faker import providers
from random import randint, choice
import sqlite3

NUMBER_STUDENTS = 30
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 150
fake_data = faker.Faker(locale = 'uk')

def create_db():
    # читаємо файл зі скриптом для створення БД
    with open('college.sql', 'r') as f:
        sql = f.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect('college.sqlite') as con:
        cur = con.cursor()
        # виконуємо скрипт із файлу, який створить таблиці в БД
        cur.executescript(sql)


def prepare_data(students, groups, subjects, teachers, grades) -> tuple():
 
    for_groups = [] 

    for group in groups:
        for_groups.append((group, ))
   
    for_students = []

    for student in students:
        *_, firstname, lastname = student.split(' ')
        for_students.append((firstname, lastname, randint(1, len(groups))))
        
    for_teachers = [] 

    for teacher in teachers:
        *_, firstname, lastname = teacher.split(' ')
        for_teachers.append((firstname, lastname))
        
    for_subjects = [] 

    for subject in subjects:
        for_subjects.append((subject, randint(1, len(teachers))))
        
    for_grades = []
    
    for grade in grades:
        for_grades.append((grade, randint(1, len(students)), randint(1, len(subjects)), fake_data.date_between_dates(datetime(2022, 1, 1), datetime(2022, 12, 31))))
        

    return for_students, for_groups, for_subjects, for_teachers, for_grades 


def generate_fake_data(number_students: int, number_groups: int, number_subjects: int, number_teachers: int, number_grades: int) -> tuple():
    fake_students = []  
    fake_groups = []  
    fake_subjects = []  
    fake_teachers = [] 
    fake_grades = []

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_groups):
        fake_groups.append(fake_data.bothify(text='Group ?#'))

    for _ in range(number_subjects):
        fake_subjects.append(fake_data.job())
        
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())
        
    for _ in range(number_grades):
        fake_grades.append(randint(4, 12))

    return fake_students, fake_groups, fake_subjects, fake_teachers, fake_grades


def insert_data_to_db(students, groups, subjects, teachers, grades) -> None:

    with sqlite3.connect('college.sqlite') as con:

        cur = con.cursor()


        sql_to_students = """INSERT INTO students(firstname, lastname, group_id)
                               VALUES (?, ?, ?)"""
        cur.executemany(sql_to_students, students)


        sql_to_groups = """INSERT INTO groups(groupname)
                               VALUES (?)"""
        cur.executemany(sql_to_groups, groups)


        sql_to_subjects = """INSERT INTO subjects(name, teacher_id)
                              VALUES (?, ?)"""
        cur.executemany(sql_to_subjects, subjects)


        sql_to_teachers = """INSERT INTO teachers(firstname, lastname)
                              VALUES (?, ?)"""
        cur.executemany(sql_to_teachers, teachers)


        sql_to_grades = """INSERT INTO grades(grade, student_id, subject_id, creat_at)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, grades)

        # Фіксуємо наші зміни в БД

        con.commit()
        
        
if __name__ == "__main__":
    create_db()
    students, groups, subjects, teachers, grades = prepare_data(*generate_fake_data(NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_SUBJECTS, NUMBER_TEACHERS, NUMBER_GRADES))
    insert_data_to_db(students, groups, subjects, teachers, grades)