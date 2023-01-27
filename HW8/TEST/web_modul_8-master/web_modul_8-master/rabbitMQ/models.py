from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField
from mongoengine import connect


connect(host=f"mongodb://127.0.0.1:27017/modul_8_RabbitMQ")


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    age = IntField()
    email = StringField(required=True)
    phoneNumber = StringField()
    country = StringField()
    sended = BooleanField(default=False)
