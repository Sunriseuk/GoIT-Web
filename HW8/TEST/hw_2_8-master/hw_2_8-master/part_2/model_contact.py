from mongoengine import Document, connect
from mongoengine.fields import StringField, EmailField, BooleanField


connect(host="mongodb://127.0.0.1:27017/my_db")


class Contacts(Document):
    name = StringField()
    email = EmailField()
    phone = StringField()
    sending = BooleanField()
    email_priority = BooleanField()
