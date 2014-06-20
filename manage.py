#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Set of some useful management commands,
    based on :py:mod:`script extension <flask_script>`
    (:py:class:`flask.ext.Manager`)

    A set of scripts, based on :py:mod:`script extension <flask.ext.script>`
    that you may find useful.

    Amount of commands will constantly grow.
    By now, there are:

    +-----------------------+-----------------------------------------------------------------+
    | **Command**           | **Result**                                                      |
    +=======================+=================================================================+
    | runserver             | Runs the Flask development server i.e. app.run()                |
    +-----------------------+-----------------------------------------------------------------+
    | shell                 | Runs interactive shell, ipython if installed                    |
    +-----------------------+-----------------------------------------------------------------+
    | init_data             | Resets the database schema and data.                            |
    +-----------------------+-----------------------------------------------------------------+
    | clean_pyc             | Removes all file:`*.pyc` files from the project folder          |
    +-----------------------+-----------------------------------------------------------------+
    | schema                | Perform database migrations (alembic)                           |
    +-----------------------+-----------------------------------------------------------------+

    .. todo::
       Add assets managements, as described in `doc <http://flask-assets.readthedocs.org/en/latest/#management-command>`_
       
    :copyright: \(c) 2012 by Roman Semirook.
    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""

import subprocess
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Shell, Manager
from app import app
from base import User
from ext import db


manager = Manager(app)
"""
The `~flask_script.Manager` object from the `Flask-Script` extension.
"""

@manager.command
def clean_pyc():
    """Removes all :file:`*.pyc` files from the project folder"""
    clean_command = "find . -name *.pyc -delete".split()
    subprocess.call(clean_command)


@manager.command
def init_data():
    """
    Resets the database schema and data.

    You need to call this to create your admin user,

    :seealso: `~manage.schema`
    """
    db.drop_all()
    db.create_all()

    admin = User(username=app.config['ADMIN_USERNAME'], email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASSWORD'])
    admin.save()

#: The `Flask-Migrate <http://flask-migrate.readthedocs.org/en/latest/>`_ database migrations command set
manager.add_command('schema', MigrateCommand)

manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': db}))

if __name__ == '__main__':
    manager.run()
