from sqlalchemy import Column, Integer, String, Date
from connect_db import Base, engine


# определение модели контакта
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)


# создание таблицы контактов
Base.metadata.create_all(bind=engine)
