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

    :copyright: \(c) 2012 by Roman Semirook.
    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""

from flask.helpers import url_for
from base import LoginForm
from ext import gravatar


def common_context():
    return {'gravatar': gravatar,
            'email_roman': 'semirook@gmail.com',
            'email_rockyroad': 'rocky.road@rocky-shore.net',
            'flask_home':'http://flask.pocoo.org',
            'flaskkit_main': 'https://github.com/semirook/flask-kit',
            'flaskkit_fork': 'https://github.com/RockyRoad29/flask-kit',
            }


def navigation():
    """
    Site navigation entries.

    :return:
    """
    main_page = {'name': 'Main',
                 'url': url_for('base.front_page'),
                 }
    info_page = {'name': 'Help',
                     'url': url_for('info.help'),
                     }
    flaskr_page = {'name': 'Flaskr',
                     'url': url_for('flaskr.index'),
                     }
    sa_blog_page = {'name': 'SA Blog',
                     'url': url_for('sa_blog.index'),
                     }

    return {'navigation': (main_page, flaskr_page, sa_blog_page, info_page)}


def common_forms():
    """
    Globally accessibles forms.
    :return:
    """
    return {'login_form': LoginForm()}
