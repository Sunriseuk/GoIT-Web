from mongoengine import Document, connect, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


connect(host="mongodb://127.0.0.1:27017/my_db")


class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
