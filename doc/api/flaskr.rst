Flaskr Blueprint Package
========================

This blueprint is a flask-kit integrated version of the Flaskr project,
a simple microblog application
provided as a tutorial example in Flask documentation.

You'll find the last versions of tutorial [here](http://flask.pocoo.org/docs/tutorial/)
and of source [here](https://github.com/mitsuhiko/flask/tree/master/examples/flaskr/).

The tutorial project
--------------------
The original project only supports one user that can create text-only entries and there are no feeds or comments,
but it still features everything you need to get started.

It is not depending on any extension or library other than the core Flask project.

This version
------------

This version is made part of a larger application structure, as a blueprint, and makes use of
popular extension like Flask-Login and Flask-SQLAlchemy, but also tries to apply recommended patterns
found in Flask's documentation.

It may also grow to implement popular features for your web application, while maintaining different flavors
as separate RCS branches. More different application templates will rather be implemented as distinct blueprints.


Submodules
----------

.. toctree::

   flaskr.models
   flaskr.forms
   flaskr.views
   flaskr.tests

Module contents
---------------

.. automodule:: flaskr
    :members:
    :undoc-members:
    :show-inheritance:
