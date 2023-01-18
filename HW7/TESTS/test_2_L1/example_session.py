from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///sqlalchemy_example.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person) # строка для sqlalchemi чтобы она лучше понимала связи

Base.metadata.create_all(engine)
Base.metadata.bind = engine

if __name__ == '__main__':
    new_person = Person(fullname="Alexander Incognito") # Экземпляр класса
    session.add(new_person) # загрузка данных в сессию

    session.commit() # загрузка экземпляра в базу данных

    new_address = Address(street_name='Stepana Giga', post_code ='36000', person=new_person)
    session.add(new_address)

    session.commit()

    person = session.query(Person).one()
    print(eval(person))
    print(person.id, person.fullname)
    addresses = session.query(Address).join(Address.person).all()
    for row in addresses:
        print(row.person.fullname)




    # for person in session.query(Person).all():
    #     print(person.name)