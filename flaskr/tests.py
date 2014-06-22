# -*- coding: utf-8 -*-

"""
    Example tests.

    :copyright: \(c) 2012 by Roman Semirook.
    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""

from flask import url_for
from flaskr import Entry
from testing import KitTestCase


class TestFlaskrBlueprint(KitTestCase):

    def setUp(self):
        super(TestFlaskrBlueprint, self).setUp()
        if self.app.login_manager._login_disabled:
            self.app.logger.warning('Login manager currently disabled. Re-enabling it to test views protection')
            self.app.login_manager._login_disabled = False

    def test_index(self):
        """
        Tests the flaskr front page success code.
        :return:
        """
        response = self.client.get(url_for('flaskr.index'), follow_redirects=True)
        self.assert200(response)

    def test_index_for_anonymous(self):
        """
        An anonymous visitor should see a "Log in" mention on the flaskr front page.

        :return:
        """
        response = self.client.get(url_for('flaskr.index'), follow_redirects=True)
        self.assertContains(response, 'Log in')

    def test_entries_page(self):
        """
        The flaskr entries listpage should load successfully.

        The 'Add Entry' form should be included only if the
        user is authenticated.
        """
        response = self.client.get(url_for('flaskr.show_entries'))
        self.assert200(response)

    def test_add_entry(self):
        """
        The flaskr 'Add Entry' form should be included only if the user is authenticated.
        """
        response = self.client.get(url_for('flaskr.show_entries'))
        self.assert200(response)
        self.assertEquals(0, response.data.count('Add a new entry'), "Add entry form shown to anonymous user")

        self.login()
        response = self.client.get(url_for('flaskr.show_entries'))
        self.assertEquals(1, response.data.count('Add a new entry'), "Add entry form not shown to authenticated user")

        # add entry
        response = self.client.post(url_for('flaskr.show_entries'),
                                    data={'title': "", 'text': "This post will live as long as the test"},
                                    follow_redirects=False)
        self.assertContains(response,'This field is required.',1)
        response = self.client.post(url_for('flaskr.show_entries'),
                                    data={'title': "Volatile test post", 'text': "This post will live as long as the test"},
                                    follow_redirects=True)
        self.assertContains(response,'form-errors.',0)

        # check entry has been added
        messages = self.flash_messages(response)
        print messages
        self.assertTrue('Added entry' in messages)
        entry = Entry.query.one()
        self.assertIsNotNone(entry)
        self.assertEquals("Volatile test post", entry.title)



    def test_post_entries_reserved(self):
        """
        An anonymous user cannot post entry data
        """
        response = self.client.post(url_for('flaskr.show_entries'),
                                    data={'title': "Illegal", 'text': "This post should not be accepted"},
                                    follow_redirects=False)
        print repr(response.headers)
        print response.data
        self.assertEquals(302, response.status_code)
        self.assertTrue(response.headers['Location'].endswith('/login?next=%2Fflaskr%2Fentries%2F'))
