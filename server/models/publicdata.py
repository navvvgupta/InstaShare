from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField
from .user import User


class PublicData(Document):
    name = StringField(required=True)
    path = StringField(required=True)
    content = StringField()
    user = ReferenceField(User, required=True)
    size = IntField()
    is_file = BooleanField(default=False)
