# -*- coding: utf-8 -*-

"""
    Good place for pluggable extensions.

    I've found it neat to define all extensions separately and bind them
    to the application at runtime.

    Unfortunately, it's possible if extension provides `init_app()` method only.
    But for some not-so-smart extensions there is some workaround.

    Look into the file for examples.


    :copyright: \(c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.

"""

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.gravatar import Gravatar
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment


#: Our `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_ database object
db = SQLAlchemy()

#: The `Flask-Assets <http://flask-assets.readthedocs.org/en/latest/>`_ :class:`~flask.ext.assets.Environment` to be later registered.
assets = Environment()

#: `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_ manager object
login_manager = LoginManager()

# Almost any modern Flask extension has special init_app()
# method for deferred app binding. But there are a couple of
# popular extensions that no nothing about such use case.

gravatar = lambda app: Gravatar(app, size=50)  # has no init_app()
toolbar = lambda app: DebugToolbarExtension(app)  # has no init_app()
