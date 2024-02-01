from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField
from .user import User  

class PublicData(Document):
    path = StringField(required=True)
    user = ReferenceField(User, required=True)
    size = IntField()
    is_folder = BooleanField(default=False)
