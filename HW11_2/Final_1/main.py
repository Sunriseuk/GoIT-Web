from fastapi import FastAPI, HTTPException, Depends, Path, Query
from sqlalchemy import extract
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from starlette import status

from models import Contact
from connect_db import get_db

app = FastAPI()

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
# class ContactSearch(BaseModel):
#     query: str


# определение схемы для контактов с предстоящим днем рождения
class ContactBirthday(BaseModel):
    id: int
    first_name: str
    last_name: str
    birthday: date


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

# функция для удаления контактов
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
def search_contacts(query: Optional[str] = Query(None, min_length=1), db: Session = Depends(get_db)):
    search_query = f"%{query}%" if query else "%"
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(search_query)) |
        (Contact.last_name.ilike(search_query)) |
        (Contact.email.ilike(search_query))
    ).all()
    return contacts


#функция для получения списка контактов с предстоящими днями рождения
@app.get("/contacts/birthday/", response_model=List[ContactBirthday])
def get_contacts_birthday(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)
        & (extract('month', Contact.birthday) == end_date.month) & (extract('day', Contact.birthday) <= end_date.day)
    ).all()
    return [
        ContactBirthday(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday
        )
        for contact in contacts
    ]