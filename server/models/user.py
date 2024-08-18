from mongoengine import Document, StringField, BooleanField


class User(Document):
    username = StringField(required=True, max_length=50, unique=True)
    password = StringField(required=True)
    is_online = BooleanField(default=False)
    ip_address = StringField(required=True, max_length=15)

    def to_dict(self):
        return {
            "username": self.username,
            "is_online": self.is_online,
            "ip_address": self.ip_address,
            # Include other fields as needed, but exclude sensitive data like passwords
        }
