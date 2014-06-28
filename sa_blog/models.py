from datetime import datetime
from base.models import CRUDMixin
from ext import db
from flask import current_app


class Post(CRUDMixin, db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    #: The post title
    title = db.Column(db.String(80), nullable=False)

    #: The post body, or article
    body = db.Column(db.Text)

    #: The publication date.
    #: Automatically set, it will not be editable by the user
    pub_date = db.Column(db.DateTime)

    #: Relationship: foreign key to category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    #: Relationship: link to the actual `Category` object
    #:               A new attribute `posts` will be dynamically
    #:               added to the target entity (backref).
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

    def update(self, form, commit=True, **kwargs):
        current_app.logger.debug('Updating post #%d', self.id)
        self.pub_date = datetime.utcnow()
        return super(Post, self).update(form, commit, **kwargs)


class Category(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name

    # def __repr__(self):
    #     return '<Category %r>' % self.name

    #: Override `__str__` for friendly display in pages.
    def __str__(self):
        return  self.name
