from marshmallow_sqlalchemy import ModelSchema
from .models import People

class PeopleSchema(ModelSchema):
    class Meta:
        model = People
