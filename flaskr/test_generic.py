#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Testing generic views.

    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""
from werkzeug.urls import url_encode

__author__ = 'rockyroad'

from flask import url_for
from flaskr import Entry
from testing import KitTestCase

ADD_FORM_HEADER = 'Add a new entry'
FAILED='Validation failed'
SUCCESS='Successfully added'


class FlaskrTestCase(KitTestCase):
    def setUp(self):
        super(FlaskrTestCase, self).setUp()
        if self.app.login_manager._login_disabled:
            self.app.logger.warning('Login manager currently disabled. Re-enabling it to test views protection')
            self.app.login_manager._login_disabled = False

    def db_addEntry(self, title="Volatile test post", text="This post will live as long as the test"):
        entry = Entry()
        entry.title=title
        entry.text=text
        entry.save()
        return entry


class TestFlaskrORM(FlaskrTestCase):
    def test_ORM(self):
        entry = self.db_addEntry()
        self.assertEquals(1,entry.id)

class TestFlaskrListViews(FlaskrTestCase):
    def setUp(self):
        FlaskrTestCase.setUp(self)
        self.url = url_for('flaskr.list')

    def test_get_ok(self):
        """
        The flaskr entries listpage should load successfully.

        """
        response = self.client.get(self.url)
        self.assert200(response)

    def test_form_display(self):
        """
        The add form should be included only if the
        user is authenticated.
        """
        response = self.client.get(self.url)
        self.assertEquals(0, response.data.count(ADD_FORM_HEADER), "Add entry form shown to anonymous user")
        self.login()
        response = self.client.get(self.url)
        self.assertEquals(1, response.data.count(ADD_FORM_HEADER), "Add entry form not shown to authenticated user")

    def test_list_anonymous_post_redirected(self):
        """
        An anomymous user post should redirect to login page
        :return:
        """
        response = self.client.post(self.url, follow_redirects=False,
                                    data={'title': "Illegal", 'text': "This post should not be accepted"},
        )
        print response.headers
        print self.flash_messages(response)
        print repr(response.headers)
        self.assertEquals(302, response.status_code)
        self.assertTrue(response.headers['Location'].endswith('/login?' + url_encode(dict(next=self.url))))

class TestFlaskrDetailViews(FlaskrTestCase):
    def setUp(self):
        FlaskrTestCase.setUp(self)
        self.url = url_for('flaskr.list')

    def test_get_ok(self):
        """
        The flaskr entries listpage should load successfully.

        """
        response = self.client.get(self.url)
        self.assert200(response)

    def test_form_display(self):
        """
        The add form should be included only if the
        user is authenticated.
        """
        response = self.client.get(self.url)
        self.assertEquals(0, response.data.count(ADD_FORM_HEADER), "Add entry form shown to anonymous user")
        self.login()
        response = self.client.get(self.url)
        self.assertEquals(1, response.data.count(ADD_FORM_HEADER), "Add entry form not shown to authenticated user")

    def test_list_anonymous_post_redirected(self):
        """
        An anomymous user post should redirect to login page
        :return:
        """
        response = self.client.post(self.url, follow_redirects=False,
                                    data={'title': "Illegal", 'text': "This post should not be accepted"},
        )
        print response.headers
        print self.flash_messages(response)
        print repr(response.headers)
        self.assertEquals(302, response.status_code)

        self.assertTrue(response.headers['Location'].endswith('/login?' + url_encode(dict(next=self.url))))
