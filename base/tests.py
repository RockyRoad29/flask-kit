# -*- coding: utf-8 -*-

"""
    Example tests.

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from flask import url_for
from testing import KitTestCase


class TestFrontBlueprint(KitTestCase):

    def test_front(self):
        """
        Tests the front page success code.
        :return:
        """
        response = self.client.get(url_for('base.front_page'))
        self.assert200(response)

    def test_front_for_anonymous(self):
        """
        An anonymous visitor should see a "Log in" mention on the front page.

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
