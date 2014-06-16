# -*- coding: utf-8 -*-
"""
Initializes the example *flaskr* blueprint and views.

"""

from flask import Blueprint

#: Defines your example blueprint
flaskr = Blueprint('flaskr', __name__,
                   template_folder='templates',
                   url_prefix='/flaskr')


from views import *
