# -*- coding: utf-8 -*-

"""
    Implements useful helpers.

    There is the application factory and, maybe,
    something else (in the future) to avoid routine.

    :copyright: \(c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.

"""

import os
import logging
from flask import Flask
from werkzeug.utils import import_string


class NoContextProcessorException(Exception):
    pass


class NoBlueprintException(Exception):
    pass


class NoExtensionException(Exception):
    pass


class AppFactory(object):
    """
    Flask application factory.

    >>> from settings import TestingConfig
    >>> app = AppFactory(TestingConfig).get_app(__name__)

    """
    def __init__(self, config, envvar='PROJECT_SETTINGS', bind_db_object=True):
        """
        Defines default application settings

        :param config: an object to load initial configuration from
        :param envvar: The name of an environment variable to update configuration from
        :param bind_db_object:
        """
        self.app_config = config
        self.app_envvar = os.environ.get(envvar, False)
        self.bind_db_object = bind_db_object

    def get_app(self, app_module_name, **kwargs):
        """
        Actually instanciates a Flask application with active settings,
        and taking care of registering extensions and blueprints

        :param app_module_name: the name of the application package, see :py:class:`~flask.Flask`

        :param kwargs: keyword arguments passed to the Flask constructor
        :return: A new WSGI application object
        """
        self.app = Flask(app_module_name, **kwargs)
        self.app.config.from_object(self.app_config)
        self.app.config.from_envvar(self.app_envvar, silent=True)

        self._setup_logging()
        self._bind_extensions()
        self._register_blueprints()
        self._register_context_processors()

        return self.app

    def _get_imported_stuff_by_path(self, path):
        """
        Splits a python object's path into `(module, object_name)`,
        and imports the module.

        For example, if `path='base.context_processors.navigation'`,
        then the whole `base.context_processors` module is imported,
        and the method returns the tuple `
        `(base.context_processors, 'navigation')

        :param path: basestring the full path of object
        :return: a tuple of
            * the imported parent module
            * the object name
        """
        module_name, object_name = path.rsplit('.', 1)
        module = import_string(module_name)

        return module, object_name

    def _bind_extensions(self):
        """


        :raise:
        """
        for ext_path in self.app.config.get('EXTENSIONS', []):
            module, e_name = self._get_imported_stuff_by_path(ext_path)
            if not hasattr(module, e_name):
                raise NoExtensionException('No {e_name} extension found'.format(e_name=e_name))
            ext = getattr(module, e_name)
            if getattr(ext, 'init_app', False):
                ext.init_app(self.app)
            else:
                ext(self.app)

    def _register_context_processors(self):
        """
        Calls :meth:`flask.Flask.context_processor` for all entries
        in the `CONTEXT_PROCESSORS` configuration value, for which defaults
        are set in :mod;`settings`.

        :return:
        """
        for processor_path in self.app.config.get('CONTEXT_PROCESSORS', []):
            module, p_name = self._get_imported_stuff_by_path(processor_path)
            if hasattr(module, p_name):
                self.app.context_processor(getattr(module, p_name))
            else:
                raise NoContextProcessorException('No {cp_name} context processor found'.format(cp_name=p_name))

    def _register_blueprints(self):
        """
        Calls :meth:`flask.Flask.register_blueprint` for all entries
        in the `BLUEPRINTS` configuration value, for which defaults
        are set in :mod;`settings`.

        .. todo::
           It is not possible for now to specify settings for the blueprint,
           e.g. `url_prefix`.

        :return:
        """
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            module, b_name = self._get_imported_stuff_by_path(blueprint_path)
            if hasattr(module, b_name):
                self.app.register_blueprint(getattr(module, b_name))
            else:
                raise NoBlueprintException('No {bp_name} blueprint found'.format(bp_name=b_name))

    def _setup_logging(self):
        self.app.logger.setLevel(self.app.config.get('LOGGING_LEVEL', logging.INFO))
        for handler in self.app.config.get('LOGGING_HANDLERS', []):
            self.app.logger.addHandler(handler)
