import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()

sql_1 = """
SELECT ROUND(AVG(p.total), 2), e.post
FROM payments as p
LEFT JOIN employees as e ON p.employee_id = e.id
GROUP BY e.post;
"""

sql_2 = """
SELECT COUNT(*), c.company_name
FROM employees e
LEFT JOIN companies c ON e.company_id = c.id
GROUP BY c.id;
"""

sql_3 = """
SELECT c.company_name, e.employee, e.post, p.total
FROM companies c
    LEFT JOIN employees e ON e.company_id = c.id
    LEFT JOIN payments p ON p.employee_id = e.id
WHERE p.total > 5000
    AND  p.date_of BETWEEN  '2021-07-10' AND  '2021-07-20'
"""

if __name__ == '__main__':
    print('--- Select First ---')
    print(execute_query(sql_1))
    print()
    print('--- Select Second ---')
    print(execute_query(sql_2))
    print()
    print('--- Select Third ---')
    print(execute_query(sql_3))