My  Flask-Kit project roadmap
=============================

Best Practices and Patterns
---------------------------

Pluggable Views
~~~~~~~~~~~~~~~
`doc <http://flask.pocoo.org/docs/views/>`_

REST api interfacing
~~~~~~~~~~~~~~~~~~~~
`Combining REST API with web interface using FLASK <http://stackoverflow.com/questions/20798582/best-practices-to-combine-rest-api-with-web-interface-using-flask>`_
may be useful in some specific cases.

`RestLess extension <http://readthedocs.org/docs/flask-restless/en/latest/>`_

Logging
~~~~~~~
`doc <http://flask.pocoo.org/docs/errorhandling/>`_

More Technologies
-----------------

DB Migration
~~~~~~~~~~~~
Miguel Grinberg presents **Flask-Migrate** in
`post <http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask>`_
the source is on
`github <https://github.com/miguelgrinberg/Flask-Migrate>`_ from Miguel Grinberg
and a rich `doc here <http://flask-migrate.readthedocs.org/en/latest/>`_ .

See also `flask-alembic <https://github.com/tobiasandtobias/flask-alembic>`_ (stalled since Feb 2013).

Note that **sqlalchemy-migrate**, originally `on google code <https://code.google.com/p/sqlalchemy-migrate/>`_ ,
is now maintained on `https://github.com/stackforge/sqlalchemy-migrate>`_ and still active.

`here <http://pythonthusiast.pythonblogs.com/230_pythonthusiast/archive/1324_flask_biography_tutorial_part_xi__managing_database_migration_in_production_environment_using_alembic.html>`_ is a tutorial not using any extension.

File Uploads
~~~~~~~~~~~~
`doc <http://flask.pocoo.org/docs/patterns/fileuploads/>`_

Caching
~~~~~~~
`doc <http://flask.pocoo.org/docs/patterns/caching/>`_
`decorator <http://flask.pocoo.org/docs/patterns/viewdecorators/#caching-decorator>`_

Ajax and JQuery
~~~~~~~~~~~~~~~
`doc <http://flask.pocoo.org/docs/patterns/jquery/>`_

Signals
~~~~~~~
`doc <http://flask.pocoo.org/docs/signals/>`_

Application Dispatching and Middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`doc <http://flask.pocoo.org/docs/patterns/appdispatch/>`_
`doc <http://flask.pocoo.org/docs/becomingbig/#wrap-with-middleware>`_

Popular extensions use
----------------------

Flask-Bootstrap : deleguate styling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`doc <http://pythonhosted.org/Flask-Bootstrap/>`_

Features
--------

Entity Relationships
~~~~~~~~~~~~~~~~~~~~

Multiple Forms per page, In-place editing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These are actually use cases where the RESTful API and the web interface application
architectures would significantly differ.

`post <http://stackoverflow.com/questions/18290142/multiple-form-in-a-single-page-using-flask-and-wtforms>`_

`in openshift tutorial <http://pythonthusiast.pythonblogs.com/230_pythonthusiast/archive/1365_flask_biography_tutorial_part_xii-implementing_profile_page_using_inline_editing.html>`_

Mail
~~~~
`FlaskMail extension <http://pythonhosted.org/Flask-Mail/>`_
