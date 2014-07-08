.. :orphan: True

Integrating Blueprints
======================

.. rubric:: Registering your blueprint

This will be done by `helpers.AppFactory`. You just need to add its name to
:data:`settings.BLUEPRINTS` .

.. rubric:: Static Resources: Assets

- add your stylesheets to :data:`app.css_base_bundle`

for example :file:`static/css/your_blueprint.css`

.. rubric:: Navigation

- add your blueprint home page to `base.context_processors.navigation` .


.. rubric:: Your blueprint initialization

:file:`your_blueprint/__init__.py`::

    # -*- coding: utf-8 -*-
    """
    Initializes the *your_blueprint* blueprint and views.

    """

    from flask import Blueprint

    #: Defines your example blueprint
    your_blueprint = Blueprint('your_blueprint', __name__,
                       template_folder='templates',
                       url_prefix='/your_blueprint')


    from views import *


.. rubric:: Your MVC architecture and tests.

- :file:`your_blueprint/models.py`
- :file:`your_blueprint/views.py`
- :file:`your_blueprint/forms.py`
- :file:`your_blueprint/tests.py`

.. rubric:: Tests first

:file:`your_blueprint/tests.py`::

    from testing import KitTestCase
    from flask import url_for

    class YourBlueprintTestCase(KitTestCase):
        """
        Put here utilities, not tests.

        """

        # def db_addEntity(self, name="Sample", description="This is a sample for testing"):
        #     "Adds a record directly to model and database"
        #     entity = Entity(name, description)
        #     entity.save()
        #     return entity

    class TestYourBluePrintPages(YourBlueprintTestCase):

        def test_index(self):
            """
            Tests the your_blueprint index page success code.
            :return:
            """
            response = self.client.get(url_for('your_blueprint.index'))
            self.assert200(response)

.. rubric:: Useful shell commands (linux)

It may be handy to define a shell variable for your blueprint name, e.g.::

    my_bp=your_blueprint

You can generate your tree structure with::

    mkdir $my_bp
    touch $my_bp/{__init__,models,views,forms,tests}.py

    xsel | sed "s/your_blueprint/$my_bp/g" > $my_bp/__init__.py

