# -*- coding: utf-8 -*-
"""
Initializes the example *info* blueprint and views.

"""

from flask import Blueprint

#: Defines your example blueprint
info = Blueprint('info', __name__,
                 template_folder='templates',
                 url_prefix='/info')


from views import *
