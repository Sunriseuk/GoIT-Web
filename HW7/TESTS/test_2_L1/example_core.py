from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select

#Создаем таблицы как класс
metadata = MetaData()

#Создаем движок для запуска sqlite в памяти компьютера
engine = create_engine('sqlite:///:memory:')

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('fullname', String),
              )

addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('email', String, nullable=False)
                  )

#Создаем таблицы
metadata.create_all(engine)

if __name__ == '__main__':
    with engine.connect() as conn:
        # ------------ Додати користувача
        new_user = users.insert().values(fullname='Alexander Incognito')
        print(new_user)
        result_insert_user = conn.execute(new_user)
        # ------------ Знайти користувача
        user_select = select(users)
        print(user_select)
        result = conn.execute(user_select)
        print(result)
        for row in result:
            print(row)
        # ------------ Додати адресу користувача
        new_address = addresses.insert().values(email='alex@gmail.com', user_id = result_insert_user.lastrowid)
        print(new_address)
        conn.execute(new_address)
        # ------------ Знайти адресу користувача
        address_select = select(addresses)
        result = conn.execute(address_select)
        print(result)
        for row in result:
            print(row)
        # ------- Join
        address_select = select(addresses.c.email, users.c.fullname).join(users)
        result = conn.execute(address_select)
        print(address_select)
        for row in result:
            print(row)