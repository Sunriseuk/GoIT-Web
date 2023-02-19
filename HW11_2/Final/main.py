from fastapi import FastAPI, HTTPException, Depends, Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, Date
from datetime import date, timedelta
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# создание приложения FastAPI
from starlette import status

app = FastAPI()

# настройка подключения к базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./contacts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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


# определение схемы контакта
class ContactSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[date]
    additional_info: Optional[str]

    class Config:
        orm_mode = True


# определение схемы для поиска контакта
class ContactSearch(BaseModel):
    query: str


# определение схемы для контактов с предстоящим днем рождения
class ContactBirthday(BaseModel):
    id: int
    first_name: str
    last_name: str
    birthday: date


# функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# функция для создания нового контакта
@app.post("/contacts/", response_model=ContactSchema)
def create_contact(contact: ContactSchema, db: Session = Depends(get_db)):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        additional_info=contact.additional_info,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# функция для получения списка всех контактов
@app.get("/contacts/", response_model=List[ContactSchema])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


# функция для получения одного контакта по идентификатору
@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# функция для обновления контакта
@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(body: ContactSchema, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.email = body.email
    contact.phone_number = body.phone_number
    contact.birthday = body.birthday
    contact.additional_info = body.additional_info
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")
    db.delete(contact)
    db.commit()


# функция для поиска контактов по имени, фамилии или адресу электронной почты
@app.get("/contacts/search/", response_model=List[ContactSchema])
def search_contacts(first_name: Optional[str] = None, last_name: Optional[str] = None,
                    email: Optional[str] = None, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(first_name) if first_name else True) &
        (Contact.last_name.ilike(last_name) if last_name else True) &
        (Contact.email.ilike(email) if email else True)
    ).all()
    return contacts


#функция для получения списка контактов с предстоящими днями рождения
@app.get("/contacts/birthday/", response_model=List[ContactBirthday])
def get_contacts_birthday(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter((Contact.birthday >= today) & (Contact.birthday <= end_date)).all()
    return [
        ContactBirthday(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday
        )
        for contact in contacts
    ]
