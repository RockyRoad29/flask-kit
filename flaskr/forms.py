from flask.ext.wtf import Form
from wtforms import fields

from wtforms.validators import DataRequired


class EntryForm(Form):
    title = fields.StringField('Post title', validators=[DataRequired()])
    text = fields.StringField('Post body')
