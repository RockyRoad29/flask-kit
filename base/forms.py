# -*- coding: utf-8 -*-

"""
    base.forms
    ~~~~~~~~~~

    The most common forms for the whole project.

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('Login', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
