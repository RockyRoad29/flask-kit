from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import widgets
from helpers import breakpoint
from sa_blog.models import Category, Post
from wtforms import StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextInput, Select,TextArea, TableWidget, ListWidget, CheckboxInput
from wtforms.fields.simple import TextField
from wtforms.validators import Optional, Length


def enabled_categories():
    return Category.query.all()

def enabled_posts():
    #breakpoint()
    return Post.query.all()

class PostForm(Form):
    title = StringField(u'title', validators=[DataRequired()])
    body = StringField(u'Text', widget=TextArea())

    # Note that pub_date is omitted, we want to set it by code

    # see http://wtforms.readthedocs.org/en/latest/ext.html#wtforms.ext.sqlalchemy.fields.QuerySelectField
    category = QuerySelectField(query_factory=enabled_categories,
                                allow_blank=True)

class CategoryForm(Form):
    name = TextField(u'Name', validators=[DataRequired(), Optional(), Length(50), ], widget=TextInput())
    posts = QuerySelectMultipleField(u'Posts', validators=[],query_factory=lambda: Post.query.all())
    # posts = QuerySelectMultipleField(u'Posts', validators=[], query_factory=lambda: Post.query.all(),
    #posts = QuerySelectMultipleField(u'Posts', validators=[], query_factory=enabled_posts,)
                                         # allow_blank=True, widget=ListWidget(),
                                         # option_widget=CheckboxInput(),
                                         # get_label=lambda p: p.title)

