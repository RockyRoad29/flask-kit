# -*- coding: utf-8 -*-

"""
    Example additional blueprint.

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask.templating import render_template
from flask.views import MethodView
from info import info


class HelpPageView(MethodView):
    "An example view for your own Blueprint"
    def get(self):
        return render_template('info/info_page.html')

info.add_url_rule('', view_func=HelpPageView.as_view('help'))
