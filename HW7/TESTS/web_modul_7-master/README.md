# SQLAlchemy ORM, alembic and argparse

"db/" has two files: "connect_db.py" - to connect sqlalchemy to PostgeSQL and in "models.py" have described sqlalchemy models. 

"seeds/" has "fill_data.py" which can fullfill the database with fake data by using library named "faker".

"queries/" has "my_select.py" which has 12 SQLAlchemy ORM queries to database.

"alembic/" has some versions(migrations) of database.

"main.py" has CLI program for CRUD database operations. It was created by used "argpase" library and SQLAlchemy ORM.




