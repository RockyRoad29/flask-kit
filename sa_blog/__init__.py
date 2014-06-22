# -*- coding: utf-8 -*-
"""
Initializes the *sa_blog* blueprint and views.

"""

from flask import Blueprint

#: Defines your example blueprint
sa_blog = Blueprint('sa_blog', __name__,
                   template_folder='templates',
                   url_prefix='/sa_blog')


from views import *
