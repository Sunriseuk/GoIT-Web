#Импортируем библиотеку
import sqlalchemy as db

#Создаем двигатель библиотеки и указываем (создаем) для нее базу данных
engine = db.create_engine('sqlite:///products-sqlalchemy.db')

#Присоеденяемся к базе данных
connection = engine.connect()

#Указываем объект-контейнер(Класс), который будет хранить информацию о таблицах (Фасад)
metadata = db.MetaData()

#Создаем таблицу и её колонки
products = db.Table('products', metadata,
                    db.Column('product_id', db.Integer, primary_key=True),#Продукт айди является Prymary_key
                    db.Column('product_name', db.Text),
                    db.Column('supplier_name', db.Text),
                    db.Column('price_per_tonne', db.Integer)
)

#Создаем таблицу (фаил бд)
metadata.create_all(engine)

#Заполняем таблицу данными
insertion_query = products.insert().values([
    {'product_name':'Banana', 'supplier_name':'United Bananas', 'price_per_tonne':7000},
    {'product_name':'Avocado', 'supplier_name':'United Avocados', 'price_per_tonne':12000},
    {'product_name':'Tomatoes', 'supplier_name':'United Tomatoes', 'price_per_tonne':3100}
])

#Вставка данных. После первой вставки данных, запрос закомментировали, чтобы каждый раз не вставлять
#connection.execute(insertion_query)

#Сохраним результат выборки
select_all_query = db.select([products])
select_all_result = connection.execute(select_all_query)

#Увидеть все результаты
# print(select_all_result.fetchall())

#Выборка с условием, где цена будет 12000 денег
select_price_query = db.select([products]).where(products.columns.price_per_tonne == 12000)
select_price_result = connection.execute(select_price_query)

# print(select_price_result.fetchall())

#Изменить значение в базе данных
update_query = db.update(products).where(products.columns.supplier_name == 'United Bananas').values(supplier_name = 'United Fruits')
connection.execute(update_query)

#Увидеть результаты
select_all_query = db.select([products])
select_all_result = connection.execute(select_all_query)

# print(select_all_result.fetchall())

#Удалить значение в базе данных
delete_query = db.delete(products).where(products.columns.supplier_name == 'United Tomatoes')
connection.execute(delete_query)

select_all_query = db.select([products])
select_all_result = connection.execute(select_all_query)

print(select_all_result.fetchall())