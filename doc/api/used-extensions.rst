.. :orphan: True

Used extensions
---------------

DebugToolbar : in-browser debug tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`Flask-DebugToolbar <http://flask-debugtoolbar.readthedocs.org/en/latest/>`_
is a port of the `Django debug toolbar <http://django-debug-toolbar.readthedocs.org/en/1.2/>`_ to Flask.


Login: user authentification layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
provides user session management for Flask.
It handles the common tasks of logging in, logging out,
and remembering your users’ sessions over extended periods of time.

It will:

   * Store the active user’s ID in the session, and let you log them in and out easily.
   * Let you restrict views to logged-in (or logged-out) users.
   * Handle the normally-tricky “remember me” functionality.
   * Help protect your users’ sessions from being stolen by cookie thieves.
   * Possibly integrate with `Flask-Principal <http://pythonhosted.org/Flask-Principal/>`_
     or other authorization extensions later on.

.. toctree::
   :maxdepth: 2

   integrate-login

SQLAlchemy : the ORM layer
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
is an extension for Flask that adds support for `SQLAlchemy <http://www.sqlalchemy.org/docs/>`_
to your application. It aims to simplify using SQLAlchemy
with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

.. toctree::
   :maxdepth: 2

   integrate-sqlalchemy

WTF : Better forms
~~~~~~~~~~~~~~~~~~

`Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_
offers simple integration with `WTForms <http://wtforms.simplecodes.com/docs/>`_

With WTForms, your form field HTML can be generated for you,
but you can customize it in your templates.
This allows you to maintain separation of code and presentation,
and keep those messy parameters out of your python code.

Testing : Unit testing for agile development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-Testing <http://pythonhosted.org/Flask-Testing/>`_
provides unit testing utilities for Flask.

Script - Command-line tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-Script <http://flask-script.readthedocs.org/en/latest/>`_
provides support for writing external scripts in Flask.
This includes running a development server, a customised Python shell,
scripts to set up your database, cronjobs, and other command-line tasks
that belong outside the web application itself.

Flask-Script works in a similar way to Flask itself.
You define and add commands that can be called from the command line to a Manager instance:

Assets - static files optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-Assets <http://flask-assets.readthedocs.org/en/latest/>`_
integrates the `webassets library <http://github.com/miracle2k/webassets>`_ with Flask, adding support for merging, minifying and compiling CSS and Javascript files.

Asset management application for Python web development - use it to merge and compress your JavaScript and CSS files.

Gravatar - User avatar on the cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flask-Gravatar <http://pythonhosted.org/Flask-Gravatar/>`_
is a small extension for Flask to make using `Gravatar <http://gravatar.com>`_
("Globally Recognized Avatar") easy.

Well, maybe not essential.
