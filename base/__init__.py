# -*- coding: utf-8 -*-
"""
Initializes the base blueprint and views.

"""
from flask import Blueprint

#: defines the base application blueprint
base = Blueprint('base', __name__,
                 template_folder='templates',
                 url_prefix='/')


from views import *
