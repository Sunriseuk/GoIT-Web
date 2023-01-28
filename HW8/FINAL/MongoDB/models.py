from mongoengine import *
from mongoengine.fields import *

#connect(host=f"mongodb+srv://mspryst:tq38bIkpcJGUCviq@cluster0.c5xjo1y.mongodb.net/HW8Database?retryWrites=true&w=majority", ssl=True)

class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = StringField()
    born_location = StringField(max_length=120)        
    description = StringField()

class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=DENY)
    quote = StringField(required=True)     
    meta = {'allow_inheritance': True}