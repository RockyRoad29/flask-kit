# -*- coding: utf-8 -*-

"""
    Example tests.

    :copyright: \(c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""
from base import User

from flask import url_for
from testing import KitTestCase


class TestFrontBlueprint(KitTestCase):

    def test_front(self):
        """
        Tests the base front page success code.
        :return:
        """
        response = self.client.get(url_for('base.front_page'))
        self.assert200(response)

    def test_front_for_anonymous(self):
        """
        An anonymous visitor should see a "Log in" mention on the base front page.

        :return:
        """
        response = self.client.get(url_for('base.front_page'))
        self.assertContains(response, 'Log in')

    def test_login(self):
        """
        The login page should load successfully.

        :return:
        """
        response = self.client.get(url_for('base.login'))
        self.assert200(response)

    def testUser(self):
        """
        The configured user should be kept in model
        """
        user1 = User.query.get(1)
        self.assertIsNotNone(user1)
        self.assertEquals(self.username, user1.username)

    def test_login_logout(self):
        """
        Login and Logout with valid credential
        """
        rv = self.login()
        self.assertTrue('You are the boss!' in self.flash_messages(rv))

        rv = self.logout()
        self.assertTrue('Login:' in rv.data)


    def test_bad_credentials(self):
        """
        Login with invalid credential should fail.
        """
        rv = self.client.post(self.login_url,
                              data=dict(email='x' + self.email, password=self.password),
                              follow_redirects=True)
        self.assertTrue('Who are you?' in self.flash_messages(rv))

        rv = self.client.post(self.login_url,
                              data=dict(email=self.email, password=self.password + 'x'),
                              follow_redirects=True)
        self.assertTrue('Who are you?' in self.flash_messages(rv))

