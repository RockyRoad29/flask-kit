# -*- coding: utf-8 -*-

"""
    The most common context processors
    for the whole project.

    Context processors inject new variables automatically into the context of a template.

    A context processor is a function that returns a dictionary.
    The keys and values of this dictionary are then merged with the template context,
    for all templates in the app.

    See [Context Processors](http://flask.pocoo.org/docs/templating/?highlight=context_processor#context-processors)
    from Flask templates documentation.

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask.helpers import url_for
from base import LoginForm
from ext import gravatar


def common_context():
    return {'gravatar': gravatar,
            'my_email': 'semirook@gmail.com'
            }


def navigation():
    """
    Site navigation entries.

    :return:
    """
    main_page = {'name': 'Main',
                 'url': url_for('base.front_page'),
                 }
    projects_page = {'name': 'Help',
                     'url': url_for('info.help'),
                     }

    return {'navigation': (main_page, projects_page)}


def common_forms():
    """
    Globally accessibles forms.
    :return:
    """
    return {'login_form': LoginForm()}
