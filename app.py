# -*- coding: utf-8 -*-

"""
Application initialization
and app-specific registrations.

There is your main app instance, created by `AppFactory`.

.. note::

    Note, it's just a point for blueprints,
    context processors and extensions binding.

    But **don't bind them explicit**, as usual.
    And **don't bind any views to the main app**.

    Why?

    You have at least two apps in your project – one as the basic app and one for testing.

    Each of them is created at runtime with some individual settings for database, debug level etc.

    And each of them has to have access to any views or extensions with their individual settings.

    So dynamical application binding is much more flexible solution.

:copyright: \(c) 2012 by Roman Semirook.
:license: BSD, see LICENSE for more details.
"""

from flask.ext.assets import Bundle
from helpers import AppFactory
from settings import DevelopmentConfig
from ext import assets


#: The :class:`Flask` application object
app = AppFactory(DevelopmentConfig).get_app(__name__)

# Assets zone

css_base_bundle = ['css/reset.css', 'css/typo.css', 'css/style.css',
                   'css/page.css', 'css/forms.css', 'css/flaskr.css']

#:Stylesheet assets bundle
css_base = Bundle(*css_base_bundle, filters='cssmin', output='gen/base.css')
assets.register('css_base', css_base)

js_base_bundle = ['js/libs/json2.js', 'js/libs/jquery-1.8.2-min.js',
                  'js/libs/underscore-1.4.2-min.js', 'js/libs/backbone-0.9.2-min.js']

#:Javascript assets bundle
js_base = Bundle(*js_base_bundle, filters='jsmin', output='gen/base.js')
assets.register('js_base', js_base)
