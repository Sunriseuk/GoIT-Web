from mongoengine import *
from mongoengine.fields import *


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    email = StringField()
    done = BooleanField(default=False)
