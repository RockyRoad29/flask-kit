Flask-SQLAlchemy Integration
============================

Here we'll go through the `extension's official documentation <http://pythonhosted.org/Flask-SQLAlchemy//>`_
(as of version 1.0)
and correlate items with flask-kit code.

Not only it should help us to master the application architecture,
but it will also help us to add features add upgrade to future
versions of the extension.

.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/quickstart.txt

Configuration
-------------
.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/config.txt

The extension provides several
`configuration keys <http://pythonhosted.org/Flask-SQLAlchemy/config.html#configuration-keys>`_

We set :data:`SQLALCHEMY_DATABASE_URI` in :mod:`settings` which will be loaded in
:data:`app.app` or :meth:`testing.KitTestCase.create_app`.

If needed, check the `Connection URI Format <http://pythonhosted.org/Flask-SQLAlchemy/config.html#connection-uri-format>`_ .

As for other extensions, the engine is instanciated in module `ext` (:data:`ext.db`) like this::

    db = SQLAlchemy()

.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/contexts.txt

Note that the application object is not supplied here.
As explained in :ref:`contexts`, the binding
can be done later by the `init_app()` method.

In *Flask-kit*, it done by the *private* method
:meth:`helpers.AppFactory._bind_extensions`
for all extensions registered
in :attr:`settings.BaseConfig.EXTENSIONS`.


Database creation (:meth:`flask.ext.sqlalchemy.SQLAlchemy.create_all`)
is done in :func:`manage.init_data` and in :meth:`testing.KitTestCase.create_app` .


Declaring Models
----------------
.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/models.txt

See :ref:`models` for full reference.

We declare our user model in :class:`base.models.User` .

Instead of inheriting only from :class:`flask.ext.sqlalchemy.Model`,
our class is also derived
from :class:`flask.ext.login.UserMixin` for :doc:`integrate-login`
as well as
from our custom :class:`base.models.CRUDMixin` (see below).

.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/queries.txt

Select, Insert, Delete
----------------------

Inserting Records
~~~~~~~~~~~~~~~~~

    Inserting data into the database is a three step process:

    1.  Create the Python object
    2.  Add it to Flask-SQLAlchemy the session
    3.  Commit the Flask-SQLAlchemy session

    >>> from yourapp import User
    >>> me = User('admin', 'admin@example.com')
    >>> db.session.add(me)
    >>> db.session.commit()

This is what is done in the :meth:`base.models.CRUDMixin.create` method,
which shares the :meth:`~base.models.CRUDMixin.save` part with
:meth:`base.models.CRUDMixin.update`,
the `commit` being optional to allow *rollback* or optimization.

The object's :attr:`~base.models.CRUDMixin.id` will be set by sqlalchemy at commit time.

Deleting Records
~~~~~~~~~~~~~~~~

    Deleting records is very similar, instead of
    :func:`~sqlalchemy.orm.session.Session.add` use
    :func:`~sqlalchemy.orm.session.Session.delete`:

    >>> db.session.delete(me)
    >>> db.session.commit()

This is what is done in the :meth:`base.models.CRUDMixin.delete` method,

Querying Records
~~~~~~~~~~~~~~~~

.. .
  Our :class:`base.models.CRUDMixin` model has only the mandatory attribute `id`,
  The primary key which theorically can be of any data type, is forced to be integer.
  Although it is commonly a cctually Fla


This is done through class methods, e.g.
  * :meth:`base.models.CRUDMixin.get_by_id`
  * :meth:`base.models.User.get_by_email`

.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/binds.txt

.. http://pythonhosted.org/Flask-SQLAlchemy/_sources/signals.txt

..