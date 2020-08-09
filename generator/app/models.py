"""mongoengine models"""

from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, ListField,BooleanField, DictField,\
                        EmbeddedDocumentField, IntField


class Variables(EmbeddedDocument):
    variable = StringField(max_length=1, required=True)
    min = IntField(required=True)
    max = IntField(required=True)
    zero_ok = BooleanField()
    num_type = StringField(max_length=1)

    def __unicode__(self):
        return self.variable


class Problems(EmbeddedDocument):
    values = DictField(required=True)
    problem = StringField(max_length=255, required=True)
    answer = StringField(max_length=255, required=True)


class Topics(Document):
    topic = StringField(max_length=255, required=True)
    instructions = StringField(max_length=255, required=True)
    categories = ListField(StringField(max_length=50), required=True)
    integers_only = BooleanField()
    positive_only = BooleanField()
    equation = StringField(max_length=255, required=True)
    variables = ListField(EmbeddedDocumentField(Variables), required=True)
    problems = ListField(EmbeddedDocumentField(Problems), required=True)

    def __unicode__(self):
        return self.topic

    def __repr__(self):
        return self.topic
