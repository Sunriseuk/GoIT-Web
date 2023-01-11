import sqlite3

with open('query_12.sql', 'r') as f:
    sql = f.read()


with sqlite3.connect('college.sqlite') as con:
    cur = con.cursor()
    cur.execute(sql, {"subject_id": 1, "group_id": 1})
    result = cur.fetchall()
    print(result)
    cur.close()