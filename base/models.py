# -*- coding: utf-8 -*-

"""
    the most common models for the whole project.

    .. rubrique: about "mixin" classes
        * http://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful
        * http://en.wikipedia.org/wiki/mixin

    :copyright: \(c) 2012 by roman semirook.
    :license: bsd, see license for more details.

"""

from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class User(UserMixin, CRUDMixin, db.Model):
    """
    A basic user model, sufficient for authorization support.

    Note that email is defined as *unique*, so we'll be able to
    find a specific user given her email (:meth:`get_by_email`).

    The primary key is inherited from :class:`CRUDMixin`
    (:attr::`CRUDMixin.id`)

    """
    __tablename__ = 'users'

    username = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return u'<User %r>' % self.username

    def check_password(self, password):
        """
        Checks a password against a given salted and hashed password value,
        using :mod:`werkzeug.security` tools

        :param password:
        :return:
        """
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_email(cls, email):
        """
        Retrieves a user from her email.

        :param cls:
        :param email:
        :return:
        """
        return cls.query.filter_by(email=email).first()
