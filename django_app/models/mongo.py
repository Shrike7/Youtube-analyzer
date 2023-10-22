from mongoengine import (Document, BooleanField, IntField, ReferenceField,
                         StringField, ListField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField)


class File(Document):
    user_id = IntField(required=True)
    status = BooleanField(default=False)


class Subtitle(EmbeddedDocument):
    name = StringField()
    url = StringField()


class Video(Document):
    status = BooleanField(default=False)
    user = IntField(required=True)
    host = ReferenceField(File)
    header = StringField()
    title = StringField()
    titleUrl = StringField()
    subtitles = ListField(EmbeddedDocumentField(Subtitle))
    time = DateTimeField()
    products = ListField(StringField())
    activityControls = ListField(StringField())


