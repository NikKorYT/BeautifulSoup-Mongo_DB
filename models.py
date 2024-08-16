from mongoengine import Document
from mongoengine.fields import (
    DateTimeField,
    ListField,
    StringField,
    ReferenceField,
    EmailField,
    BooleanField,
)


class authors(Document):
    full_name = StringField(required=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class qoutes(Document):
    tags = ListField(StringField())
    author = ReferenceField(authors)
    quote = StringField(required=True)


class users(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    message_sent_status = BooleanField(required=True, default=False)
