# -*- coding: utf-8 -*-

"""
    the most common models for the whole project.

    .. rubrique: about "mixin" classes
        * http://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful
        * http://en.wikipedia.org/wiki/mixin

    :copyright: \(c) 2012 by roman semirook.
    :license: bsd, see license for more details.

"""
from flask import current_app

from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db
from wtforms.ext.sqlalchemy.orm import model_fields
from wtforms.form import BaseForm


class CRUDMixin(object):
    """
    Base class for all model objects, providing ORM layer,
    as proposed in :mod:`flask.ext.sqlalchemy` documentation.

    Note that it is not based on :class:`flask.ext.sqlalchemy.Model`,
    but assumes the actual instance is, using
    its :attr:`flask.ext.sqlalchemy.Model.query` property
    ( a :class:`flask.ext.sqlalchemy.BaseQuery` instance ).

    .. seealso::
       You may want to read more about *python Mixin pattern*, or
       *dynamic inheritance* or `metaclasses <https://www.python.org/doc/essays/metaclasses/>`_.

    .. todo:: Add a query_all() class method

    """
    __table_args__ = {'extend_existing': True}

    #id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieved a record by primary key.
        @deprecated Removed: the integer pk and name restriction seems pointless.
        :param id: a pk integer compatible value
        """
        raise NotImplementedError("This method has been removed. use `model.query.get()` instead.")

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new model instance, with the given keyword parameters,
        and immediately persists it to the database, hence assigning
        a value to its :attr:`id' attribute (primary key).

        :param kwargs:
        """
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """
        Modifies instance attributes as specified in keyword arguments,
        and immediately save it two the active database session.

        :param commit: set this to False to avoid committing database changes.
        :param kwargs: whatever fields you need to update

        :return: self
        """
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """
        Adds the instance to the database and optionnally
        commit the session.
        :param commit:
        :return:
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, form, commit=True):
        """
        Updates the instance to the database and optionnally
        commit the session.
        :param commit:
        :return:
        """
        assert(isinstance(form, BaseForm))
        form.populate_obj(self)
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """
        Removes the instance to the database and optionnally
        commit the session.

        .. todo:: Maybe clear the id attribute to mark the object invalid.

        :param commit:
        :return:
        """
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_fields(cls):
        """
        @deprecated form iterator does this better.
        """
        current_app.logger.warning('@DEPRECATED Generating field list by schema introspection, order is random')
        return [ k for k in model_fields(cls, db_session=db) if k != 'id']

class User(UserMixin, CRUDMixin, db.Model):
    """
    A basic user model, sufficient for authorization support.

    Note that email is defined as *unique*, so we'll be able to
    find a specific user given her email (:meth:`get_by_email`).

    The primary key is inherited from :class:`CRUDMixin`
    (:attr:`CRUDMixin.id`)

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, email, password):
        """
        Object constructor.
        Password is stored encrypted through
        :meth:`werzeug.security.generate_password_hash`
        
        :param username:
        :param email:
        :param password:
        """
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
