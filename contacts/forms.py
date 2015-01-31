# -*- coding: utf-8 -*-
# Generated by RockyRoad's form_generator
#
# Ok, it still will need some correction, e.g. for lambdas,
# but it should be a good start.
#
# If the result doesn't fit what you expect,
# it might means that you should adjust your model definition.
from contacts.models import Email
from flask_wtf.form import Form
from wtforms.fields.core import DateField, FieldList, StringField, FormField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.widgets.core import TextInput, ListWidget, TableWidget
from wtforms.validators import DataRequired, Optional, Length
# Flask's form inherits from wtforms.ext.SecureForm by default
# this is the WTForm base form.
from wtforms import Form as WTForm

# Never render this form publicly because it won't have a csrf_token
class EmailForm(Form):
    email = EmailField(u'Email')

    status = SelectField(u'Status', validators=[DataRequired(), ],
                         choices=[('active', 'Active'), ('suspended', 'Suspended'), ('error', 'Error')],
                         default='active',
    )
    #notes = StringField(u'Notes', validators=[Optional(), ], widget=TextInput()())


    # contact = QuerySelectField(u'Contact', validators=[],
    #                            )
    # {get_label: !!python/name:wtforms.ext.sqlalchemy.fields.%3Clambda%3E '', get_pk: !!python/name:wtforms.ext.sqlalchemy.fields.get_pk_from_identity '',
    #   query_factory: !!python/name:wtforms.ext.sqlalchemy.orm.%3Clambda%3E ''}


def no_duplicate_email(form, field):
    """

    @TODO test if no duplicate email is in field list
    @see http://wtforms.readthedocs.org/en/latest/validators.html#custom-validators

    :return:
    """
    return True
    #  or raise ValidationError(message)


class ContactForm(Form):
    first_name = StringField(u'First Name', validators=[Optional(), Length(max=80), ], widget=TextInput())
    last_name = StringField(u'Last Name', validators=[DataRequired(), Length(max=80), ], widget=TextInput())
    date_of_birth = DateField(u'Date Of Birth', validators=[Optional(), ], widget=TextInput())
    # {format: !!python/unicode '%Y-%m-%d'}

    #notes = StringField(u'Notes', validators=[Optional(), ], widget=TextInput())
    # Render a collection of subforms in a table, each subform being a list
    emails = FieldList(FormField(EmailForm, widget=ListWidget()), widget=TableWidget(),
                       validators=[no_duplicate_email])

