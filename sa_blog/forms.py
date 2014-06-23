from flask.ext.wtf import Form
from sa_blog.models import Category
from wtforms import StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


def enabled_categories():
    return Category.query.all()


class PostForm(Form):
    title = StringField(u'title', validators=[DataRequired()])
    body = StringField(u'Text', widget=TextArea())

    # Note that pub_date is omitted, we want to set it by code

    # see http://wtforms.readthedocs.org/en/latest/ext.html#wtforms.ext.sqlalchemy.fields.QuerySelectField
    category = QuerySelectField(query_factory=enabled_categories,
                                allow_blank=True)
