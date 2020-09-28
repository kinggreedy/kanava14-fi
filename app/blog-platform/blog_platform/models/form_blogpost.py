from wtforms import Form, StringField, TextAreaField, validators
from wtforms import IntegerField
from wtforms.widgets import HiddenInput
from .form_registration import strip_filter


class BlogPostFormCreate(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Content', [validators.Length(min=1)],
                         filters=[strip_filter])


class BlogPostFormUpdate(BlogPostFormCreate):
    id = IntegerField(widget=HiddenInput())
