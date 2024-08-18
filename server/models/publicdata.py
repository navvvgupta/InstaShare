from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField
from .user import User


class PublicData(Document):
    name = StringField(required=True)
    path = StringField(required=True)
    content = StringField()
    user = ReferenceField(User, required=True)
    size = IntField()
    is_file = BooleanField(default=False)

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "content": self.content,
            "user": str(
                self.user.id
            ),  # Convert the user reference to a string ID or any other relevant representation
            "size": self.size,
            "is_file": self.is_file,
        }
