from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, DateField, ReferenceField
from mongoengine import connect

connect(host=f"mongodb://127.0.0.1:27017/modul_8")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()