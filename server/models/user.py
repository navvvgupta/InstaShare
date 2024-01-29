from mongoengine import Document, StringField, BooleanField

class User(Document):
    username = StringField(required=True, max_length=50,unique=True)
    password = StringField(required=True)
    is_online = BooleanField(default=False)
    ip_address = StringField(required=True, max_length=15) 
    
