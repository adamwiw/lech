from mongoengine import Document, ListField, StringField


class Question(Document):
    question = StringField()
    answer = StringField()
    answers = ListField(StringField())
