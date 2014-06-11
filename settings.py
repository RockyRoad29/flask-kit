# -*- coding: utf-8 -*-

"""
Global settings for project.

Note some Kit-specific settings.

  * `BLUEPRINTS` is a list of registered blueprints.
  * `CONTEXT_PROCESSORS` is a list of registered context processors.
  *     `EXTENSIONS` is a list of registered extensions.

Flask Kit will automatically register blueprints specified in the `BLUEPRINTS`
list for you. Behaviour for `CONTEXT_PROCESSORS` and `EXTENSIONS` lists is the same.

The notation is `package.module.object` or `package.object` if object is in the `__init__.py`.
Look into the file for examples.

:seealso: http://flask.pocoo.org/docs/config/#configuration-best-practices

    :copyright: \(c) 2012 by Roman Semirook.
    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""

import os


class BaseConfig(object):
    """
    see also: :py:attr:`flask.Flask.default_config`
    """
    DEBUG = False
    SECRET_KEY = "MY_VERY_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    BLUEPRINTS = ['base.base',
                  'info.info',
                  ]
    "a list of registered blueprints."

    EXTENSIONS = ['ext.db',
                  'ext.assets',
                  'ext.login_manager',
                  'ext.gravatar',
                  'ext.toolbar',
                  ]
    "a list of registered extensions."

    CONTEXT_PROCESSORS = ['base.context_processors.common_context',
                          'base.context_processors.navigation',
                          'base.context_processors.common_forms',
                          ]
    "a list of registered context processors"

class DevelopmentConfig(BaseConfig):
    """
    During development, we want to enable debugging and profiling.
    """
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(BaseConfig):
    """
    Designed for running tests, it uses an in-memory sqlite database.

    >>> app = AppFactory(TestingConfig).get_app("my-tests")
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
