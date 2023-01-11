import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT students.firstname AS firstname, students.lastname AS lastname, subjects.name AS subject
FROM students AS students
    INNER JOIN grades AS grades ON students.id = grades.student_id
    INNER JOIN subjects AS subjects ON grades.subject_id = subjects.id
ORDER BY students.lastname, students.firstname
"""

if __name__ == '__main__':
    print(execute_query(sql))