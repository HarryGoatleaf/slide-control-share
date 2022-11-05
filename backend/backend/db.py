from mongoengine import *

class User(Document):
    name = StringField(max_length=32, required=True)
    
    def encode(self):
        return {'id': str(self.id), 'name': self.name}
    
class Presentation(Document):
    host = ReferenceField(User, required=True)
    users  = ListField(ReferenceField(User), required=False)
    slides = FileField()
    current_slide = IntField(required=True)
    
    def encode(self):
        print(self.users[0].encode())
        return {
            'id': str(self.id),
            'host': self.host.encode(),
            'users': [u.encode() for u in self.users],
            'current_slide': self.current_slide,
        }