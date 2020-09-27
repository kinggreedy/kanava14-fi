from wtforms import Form, StringField, validators
from wtforms import PasswordField


def strip_filter(x): return x.strip() if x else None


class RegistrationForm(Form):
    username = StringField('Username',
                           [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3)])
    name = StringField('Name', filters=[strip_filter])
