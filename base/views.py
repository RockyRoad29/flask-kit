# -*- coding: utf-8 -*-

"""
    The most common views for the whole project.

    This makes use of flask's [pluggable views](http://flask.pocoo.org/docs/views/)

    :copyright: \(c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask.templating import render_template
from flask.views import MethodView
from flask import flash, redirect, request, url_for, current_app
from flask.ext.login import login_user, login_required, logout_user
from ext import login_manager
from base import base
from base.forms import LoginForm
from base.models import User

class FrontView(MethodView):
    """
    Tha application front page.

    Just renders the template :file:`templates/base/main.html`
    """
    def get(self):
        return render_template('base/main.html')

base.add_url_rule('', view_func=FrontView.as_view('front_page'))


class LoginView(MethodView):
    _messages = {'success': 'You are the boss!',
                 'invalid_auth': 'Who are you?',
                 'invalid_data': 'Invalid data.',
                 }

    def get(self):
        """
        Handles the HTTP GET requests (overriding :meth:`MethodView.get`) .
        :return: The rendered login form page.
        """
        return render_template('login.html', form=LoginForm())

    def post(self):
        """
        Handles the HTTP POST requests (overriding :meth:`MethodView.post`) .

        If the form was correctly filled and the user password validates
        (through :meth:`~base.models.User.check_password`),
        calls :func:`flask.ext.login.login_user`,
        emits a flash message of success and redirects the request to
        the `next` parameter or the home page if not specified.

        Otherwise, emits errors as flash messages and renders the login page again.

        :return: On error, renders the login page, but redirects to value of `next` or home page on success.
        """
        form = LoginForm()
        if not form.validate_on_submit():
            flash(self._messages['invalid_data'])
            return render_template('login.html', form=form)

        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(self._messages['success'])
        else:
            flash(self._messages['invalid_auth'])
            return redirect(url_for('base.login'))

        return redirect(request.args.get('next') or url_for('base.front_page'))

base.add_url_rule('login', view_func=LoginView.as_view('login'))


login_manager.login_view = 'base.login'
login_manager.login_message = 'You have to log in to access this page.'


@login_manager.user_loader
def load_user(user_id):
    """
    We need to provide a :meth:`~flask.ext.login.LoginManager.user_loader` callback to the login manager.
    This callback is used to reload the user object from the user ID stored in the session.

    It should return `None` (**not raise an exception**) if the ID is not valid.
    (In that case, the ID will manually be removed from the session and processing
    will continue.)

    This is done by calling :meth:`~base.models.User.get_by_id`)
    ,
    :param user_id: the unicode ID of a user
    :return:the corresponding user object
    """
    return User.get_by_id(user_id)


@login_required
def logout():
    """
    calls func:`flask.ext.login.logout_user`, and redirects to home page.

    :return: redirects to home page
    """
    logout_user()
    return redirect(url_for('base.front_page'))

base.add_url_rule('logout', view_func=logout, methods=['POST'])

@base.route("site-map")
def site_map():
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods:
            if rule.arguments and (not rule.defaults or len(rule.defaults) < len(rule.arguments)):
                continue
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return render_template('sitemap.html', links=sorted(links, key=lambda x: x[1]))
