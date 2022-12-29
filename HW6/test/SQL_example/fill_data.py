from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_COMPANIES = 3
NUMBER_EMPLOYESS = 30
NUMBER_POST = 5


def generate_fake_data(number_companies, number_employees, number_post) -> tuple():
    fake_companies = []  # здесь будем хранить компании
    fake_employees = []  # здесь будем хранить сотрудников
    fake_posts = []  # здесь будем хранить должности
    '''Возьмём три компании из faker и поместим их в нужную переменную'''
    fake_data = faker.Faker()

    # Создадим набор компаний в количестве number_companies
    for _ in range(number_companies):
        fake_companies.append(fake_data.company())

    # Сгенерируем теперь number_employees количество сотрудников'''
    for _ in range(number_employees):
        fake_employees.append(fake_data.name())

    # И number_post набор должностей
    for _ in range(number_post):
        fake_posts.append(fake_data.job())

    return fake_companies, fake_employees, fake_posts


def prepare_data(companies, employees, posts) -> tuple():
    for_companies = []
    # подготавливаем список кортежей названий компаний
    for company in companies:
        for_companies.append((company, ))

    for_employees = []  # для таблицы employees

    for emp in employees:
        '''
        Для записей в таблицу сотрудников нам надо добавить должность и id компании. Компаний у нас было по умолчанию
        NUMBER_COMPANIES, при создании таблицы companies для поля id мы указывали INTEGER AUTOINCREMENT - потому каждая 
        запись будет получать последовательное число увеличенное на 1, начиная с 1. Потому компанию выбираем случайно
        в этом диапазоне 
        '''
        for_employees.append((emp, choice(posts), randint(1, NUMBER_COMPANIES)))

    '''
    Похожие операции выполним и для таблицы payments выплаты зарплат. Примем, что выплата зарплаты во всех компаниях 
    выполнялась с 10 по 20 числа каждого месяца. Вилку зарплат будем генерировать в диапазоне от 1000 до 10000 у.е. 
    для каждого месяца, и каждого сотрудника. 
    '''
    for_payments = []

    for month in range(1, 12 + 1):
        # Выполняем цикл по месяцам'''
        payment_date = datetime(2021, month, randint(10, 20)).date()
        for emp in range(1, NUMBER_EMPLOYESS + 1):
            # Выполняем цикл по количеству сотрудников
            for_payments.append((emp, payment_date, randint(1000, 10000)))

    return for_companies, for_employees, for_payments


def insert_data_to_db(companies, employees, payments) -> None:
    # Создадим соединение с нашей БД и получим объект курсора для манипуляций с данными

    with sqlite3.connect('salary.db') as con:

        cur = con.cursor()

        '''Заполняем таблицу компаний. И создаем скрипт для вставки, где переменные, которые будем вставлять отметим 
        знаком заполнителя (?) '''

        sql_to_companies = """INSERT INTO companies(company_name)
                               VALUES (?)"""

        '''Для вставки сразу всех данных воспользуемся методом executemany курсора. Первым параметром будет текст 
        скрипта, а вторым данные (список кортежей).'''

        cur.executemany(sql_to_companies, companies)

        # Далее вставляем данные о сотрудниках. Напишем для него скрипт и укажем переменные

        sql_to_employees = """INSERT INTO employees(employee, post, company_id)
                               VALUES (?, ?, ?)"""

        # Данные были подготовлены заранее, потому просто передаем их в функцию

        cur.executemany(sql_to_employees, employees)

        # Последней заполняем таблицу с зарплатами

        sql_to_payments = """INSERT INTO payments(employee_id, date_of, total)
                              VALUES (?, ?, ?)"""

        # Вставляем данные о зарплатах

        cur.executemany(sql_to_payments, payments)

        # Фиксируем наши изменения в БД

        con.commit()


if __name__ == "__main__":
    companies, employees, posts = prepare_data(*generate_fake_data(NUMBER_COMPANIES, NUMBER_EMPLOYESS, NUMBER_POST))
    insert_data_to_db(companies, employees, posts)