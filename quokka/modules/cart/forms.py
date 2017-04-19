from quokka.core.models.content import Content

from wtforms import Form, fields
from flask_mongoengine.wtf.orm import model_form

class AddNewProductTypeForm(Form):
    description = fields.StringField()
    weight = fields.FloatField()
    dimensions = fields.StringField()


def get_content_form():
    return model_form(Content)
