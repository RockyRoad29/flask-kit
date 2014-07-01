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
import flask

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.gravatar import Gravatar
from flask.ext.login import LoginManager
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from flask.ext.migrate import Migrate


#: Our `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_ database object
db = SQLAlchemy()

#: The `Flask-Migrate <http://flask-migrate.readthedocs.org/en/latest/>`_ database migrations engine
migrate = Migrate()

#: The `Flask-Assets <http://flask-assets.readthedocs.org/en/latest/>`_ :class:`~flask.ext.assets.Environment` to be later registered.
assets = Environment()

#: `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_ manager object
login_manager = LoginManager()

# Almost any modern Flask extension has special init_app()
# method for deferred app binding. But there are a couple of
# popular extensions that no nothing about such use case.

gravatar = lambda app: Gravatar(app, size=50)  # has no init_app()
toolbar = lambda app: DebugToolbarExtension(app)  # has no init_app()


api_manager = APIManager()
#init_api_manager = lambda app: api_manager.init_app(app, flask_sqlalchemy_db=db) # needs db as init_app argument
def init_api_manager(app):
    """


    :type app: flask.Flask
    :param app:
    """
    assert(isinstance(app, flask.Flask))
    print "Initializing API for %r" % (app,)
    import contacts

    api_manager.init_app(app, flask_sqlalchemy_db=db) # needs db as init_app argument
    contacts.api_contact = api_manager.create_api_blueprint(contacts.models.Contact,
                                                            methods=['GET', 'POST', 'PATCH', 'DELETE'],
                                                            url_prefix='/api/v0')
    # the url for listing contacts will be: $HOST:$PORT/api/v0/contact
