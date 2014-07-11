# -*- coding: utf-8 -*-

"""
    More useful TestCase for tests.

    Simple basic TestCase for your tests. Note, that `nose` test runner is used (it's really good)::

        (flaskit)MacBook-Pro-Roman:flaskit semirook$ nosetests
        ...
        ----------------------------------------------------------------------
        Ran 3 tests in 0.476s

        OK


    :copyright: \(c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.

"""
from flask.ext.testing import TestCase
from base import User
from helpers import AppFactory
from settings import TestingConfig
from ext import db


class KitTestCase(TestCase):

    username = 'John Doe'
    email = 'john@doe.com'
    password = 'test'
    login_url = '/login'
    logout_url = '/logout'

    def create_app(self):
        return AppFactory(TestingConfig).get_app(__name__)

    def setUp(self):
        # Create main database, leaving binds alone.
        db.create_all(bind=None)
        self.user = User(username=self.username, email=self.email, password=self.password)
        self.user.save()

    def tearDown(self):
        db.session.remove()
        # Clean main database, leaving binds alone.
        db.drop_all(bind=None)

    def assertContains(self, response, text, count=None,
                       status_code=200, msg_prefix=''):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(response.status_code, status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
                         " (expected %d)" % (response.status_code, status_code))

        real_count = response.data.count(text)
        if count is not None:
            self.assertEqual(real_count, count,
                msg_prefix + "Found %d instances of '%s' in response"
                             " (expected %d)" % (real_count, text, count))
        else:
            self.assertTrue(real_count != 0,
                msg_prefix + "Couldn't find '%s' in response" % text)

    def login(self):
        return self.client.post(self.login_url, data=dict(
            email=self.email,
            password=self.password
        ), follow_redirects=True)

    def logout(self):
        return self.client.post(self.logout_url, follow_redirects=True)

    def flash_messages(self,response):
        from StringIO import StringIO
        stri = StringIO(response.data)
        div = None
        while True:
            nl = stri.readline()
            if nl == '': return None
            if '<div class="l-75-c flash-messages">' in nl:
                div = nl
                break
        while True:
            nl = stri.readline()
            if nl == '': return None
            div += nl
            if '</div>' in nl: break
        return div

