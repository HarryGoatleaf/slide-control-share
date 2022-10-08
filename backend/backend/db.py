from mongoengine import *

class User(Document):
    name = StringField(max_length=32, required=True)
    
class Presentation(Document):
    host = ReferenceField(User, required=True)
    users  = ListField(ReferenceField(User), required=True)
    content = StringField(max_length=1000, required=True)
    current_slide = IntField(required=True)