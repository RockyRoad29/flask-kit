# -*- coding: utf-8 -*-
"""
Initializes the *contacts* blueprint and views.

"""

from flask import Blueprint

#: Defines your example blueprint
contacts = Blueprint('contacts', __name__,
                   template_folder='templates',
                   url_prefix='/contacts')


from views import *