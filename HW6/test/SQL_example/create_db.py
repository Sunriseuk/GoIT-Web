import sqlite3


def create_db():
    # читаем файл со скриптом для создания БД
    with open('salary.sql', 'r') as f:
        sql = f.read()

    # создаем соединение с БД (если ее нет, она создастся)
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        # выполняем скрипт из файла, который создаст таблицы в БД
        cur.executescript(sql)


if __name__ == "__main__":
    create_db()