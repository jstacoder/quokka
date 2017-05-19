from us import STATES
from wtforms import fields, validators, widgets, Form
from wtforms.fields.html5 import TelField, EmailField
from flask_admin.contrib.mongoengine.fields import MongoImageField

class TestForm(Form):
    image = MongoImageField()

class AddressForm(Form):
    
    state_choices = map(
        lambda state: state.abbr,
        STATES
    )

    street1 = fields.StringField()
    street2 = fields.StringField()
    city = fields.StringField()
    state = fields.SelectField(choices=zip(state_choices,state_choices))
    zipcode = fields.IntegerField()

class CreateContactInfoForm(Form):
    title = fields.StringField()
    user_id = fields.HiddenField()
    phone_number = TelField("Phone Number", validators=[validators.Optional()])
    email = EmailField("Email Address", validators=[validators.Optional(),validators.Email()])
    message = fields.TextAreaField()
    address = fields.FormField(AddressForm)

