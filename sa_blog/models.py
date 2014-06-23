from datetime import datetime
from base.models import CRUDMixin
from ext import db


class Post(CRUDMixin, db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    # All arguments must be optional for generic instanciation
    def __init__(self, title=None, body=None, category=None, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    # def __repr__(self):
    #     return '<Category %r>' % self.name

    #: Override `__str__` for friendly display in pages.
    def __str__(self):
        return  self.name
