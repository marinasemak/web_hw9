from mongoengine import (CASCADE, DateField, Document, ListField,
                         ReferenceField, StringField)


class Author(Document):
    fullname = StringField(required=True, max_length=120, unique=True)
    born_date = DateField()
    born_location = StringField(max_length=150)
    description = StringField()

    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()

    meta = {"collection": "quotes"}
