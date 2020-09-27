from wtforms import Form, StringField, TextAreaField, validators
from wtforms import IntegerField
from wtforms.widgets import HiddenInput


def strip_filter(x): x.strip() if x else None


class BlogPostFormCreate(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])


class BlogPostFormUpdate(BlogPostFormCreate):
    id = IntegerField(widget=HiddenInput())
