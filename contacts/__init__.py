# -*- coding: utf-8 -*-
"""
Initializes the *contacts* blueprint and views.

"""

from flask import Blueprint

#: Defines blueprint
from contacts import models

contacts = Blueprint('contacts', __name__,
                     template_folder='templates',
                     url_prefix='/contacts')

#: API blueprints will be created in `ext` during app initialization.
api_contact = None
#api = {}


from views import *