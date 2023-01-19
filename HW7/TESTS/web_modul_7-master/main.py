import sys
import os
from datetime import datetime
import argparse
import sqlalchemy
from sqlalchemy.sql import select, update, insert, delete
sys.path.append(os.getcwd())

from db.models import Class, Student, Teacher, Subject, Grade
from db.connect_db import conn

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--action", choices=['create', 'list', 'update', 'remove'], required=True)
parser.add_argument("-m", "--model", choices=['Class', 'Student', 'Teacher', 'Subject', 'Grade'], required=True)
parser.add_argument("-id", "--id", type=int, default=None)
parser.add_argument("-n", "--name", type=str, default=None)
parser.add_argument("-fn", "--fullname", type=str, default=None)
parser.add_argument("-ci", "--class_id", type=int, default=None)
parser.add_argument("-ti", "--teacher_id", type=int, default=None)
parser.add_argument("-sui", "--subject_id", type=int, default=None)
parser.add_argument("-si", "--student_id", type=int, default=None)
parser.add_argument("-g", "--grade", type=int, default=None)
parser.add_argument("-d", "--date_of", type=str, default=None)

args = parser.parse_args()

def execute_query(args):

    if args.action == "list":
        query = eval(f"select({args.model})")

    elif args.action == "create":
        model = args.model
        if model == "Class":
            values = f"name='{args.name}'"
        elif model == "Student":
            values = f"fullname='{args.fullname}', class_id={args.class_id}"
        elif model == "Teacher":
            values = f"fullname='{args.fullname}'"
        elif model == "Subject":
            values = f"name='{args.name}', teacher_id={args.teacher_id}"
        elif model == "Grade":
            values = f"grade={args.grade}, date_of=datetime.strptime('{args.date_of}', '%Y-%M-%d').date(), student_id={args.student_id}, subject_id={args.subject_id}"
        query = eval(f"insert({args.model}).values({values})")

    elif args.action == "update":
        model = args.model
        if model == "Class":
            values = f"name='{args.name}'"
        elif model == "Student":
            values = f"fullname='{args.fullname}'"
        elif model == "Teacher":
            values = f"fullname='{args.fullname}'"
        elif model == "Subject":
            values = f"name='{args.fullname}'"
        elif model == "Grade":
            values = f"grade={args.grade}"
        
        query = eval(f"update({args.model}).values({values}).where(eval(f'{args.model}.id=={args.id}'))")

    elif args.action == "remove":
        query = eval(f"delete({args.model}).where(eval(f'{args.model}.id=={args.id}'))")

    return conn.execute(query)


if __name__ == '__main__':
    for r in execute_query(args):
        print(r)
    

    # actions = {"create": "insert", "list": "select", "update": "update", "remove": "delete"}
    # tables = {"Class": "classes", "Student": "students", "Teacher": "teachers", "Subject": "subjects", "Grade": "grades"}
    # models = {"Class": Class, "Student": Student, "Teacher": Teacher, "Subject": Subject, "Grade": Grade}
