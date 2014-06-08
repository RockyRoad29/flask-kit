# -*- coding: utf-8 -*-

"""
    The most common views for the whole project.

    This makes use of flask's [pluggable views](http://flask.pocoo.org/docs/views/)

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask.templating import render_template
from flask.views import MethodView
from flask import flash, redirect, request, url_for
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
                 'invalid_form': 'Invalid form.',
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

        Otherwise, emits errors as flash messages and redirects to the login page again.

        :return: redirects to login page on error, value of `next` or home page on success.
        """
        form = LoginForm()
        if not form.validate_on_submit():
            flash(self._messages['invalid_form'])
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
    Implements :meth:`flask.ext.login.LoginManager.user_loader`
    by calling :meth:`~base.models.User.get_by_id`)
    ,
    :param user_id:
    :return:
    """
    return User.get_by_id(user_id)


@login_required
def logout():
    """
    calls func:`flask.ext.login.login_user`, and redirects to home page.

    :return: redirects to home page
    """
    logout_user()
    return redirect(url_for('base.front_page'))

base.add_url_rule('logout', view_func=logout, methods=['POST'])
