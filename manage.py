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
    | assets                | Assets (static files) management                                |
    +-----------------------+-----------------------------------------------------------------+


    .. rubric:: Schema Management

    See `Flask-Migrate <http://flask-migrate.readthedocs.org/en/latest/>`_ (:py:mod:`flask.ext.migrate`)
    and `Alembic <http://alembic.readthedocs.org/en/latest>`_ documentations.

    .. rubric:: Assets Management

    Example session::

        (.venv)$ ./manage.py  assets
        usage: manage.py assets [-h] [-v] [-q] [--parse-templates]
                                {watch,build,clean,check} ...

        Manage assets.

        positional arguments:
          {watch,build,clean,check}

        optional arguments:
          -h, --help            show this help message and exit
          -v                    be verbose
          -q                    be quiet
          --parse-templates     search project templates to find bundles

        (.venv)$ ./manage.py  assets -v check
        Checking asset: gen/base.js
        Checking asset: gen/base.css
        (.venv)$ ./manage.py  assets -v clean
        Cleaning generated assets...
        Deleted asset: gen/base.js
        Deleted asset: gen/base.css
        (.venv)$ ./manage.py  assets -v --parse-templates check
        Searching templates...
        Checking asset: gen/base.js
          needs update
        Checking asset: gen/base.css
          needs update
        (.venv)$ ./manage.py  assets -v --parse-templates build
        Searching templates...
        Building bundle: gen/base.js
        Building bundle: gen/base.css
        (.venv)$ ./manage.py  assets -v --parse-templates check
        Searching templates...
        Checking asset: gen/base.js
        Checking asset: gen/base.css

    :copyright: \(c) 2012 by Roman Semirook.
    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""

import subprocess
from flask import url_for
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Shell, Manager
from app import app
from base import User
from ext import db
from scripts.form_generator import forms4package


manager = Manager(app)
"""
The `~flask_script.Manager` object from the `Flask-Script` extension.
"""

manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': db}))

#: The `Flask-Migrate <http://flask-migrate.readthedocs.org/en/latest/>`_ database migrations command set
manager.add_command('schema', MigrateCommand)

# Add assets managements, as described in `doc <http://flask-assets.readthedocs.org/en/latest/#management-command>`_
manager.add_command("assets", ManageAssets())  # assets_env={'app': app}

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

@manager.command
def list_routes():
    """
    Thanks to Jonathan on http://stackoverflow.com/a/19116758/2219061

    :return:
    """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        # for python3 use: urllib.parse.unquote()
        output.append(line)

    for line in sorted(output):
        print(line)

@manager.command
def list_routes2():
    """
    Thanks to jjia6395 on http://stackoverflow.com/a/22651263/2219061

    This version shows full rule instead of using url_for which would
    break if your arguments are not string e.g. float.
    :return:
    """
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)

@manager.option('-n', '--blueprint', dest='blueprint', default='base',
                help="Give the package name for the blueprint'")
@manager.command
def gen_forms(blueprint):
    """
    Generates forms from models using SQLAlchemy, then
    inspects the result to output suitable python form definition,
    ready to customize.

    The :file:`forms.py` is not changed (nor any file)
    unless you redirect standard output like this::

    ./manage.py gen_forms your_blueprint > your_blueprint/forms.py
    """
    print forms4package(blueprint)



if __name__ == '__main__':
    manager.run()
