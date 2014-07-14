#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: {}
"""
Testing Contacts RESTful API
"""
import unittest
import json
from flask import url_for

from testing import KitTestCase

__author__ = 'rockyroad'


class TestContactsAPI(KitTestCase):
    headers = {'Content-Type': 'application/json'}

    def __init__(self, methodName='runTest'):
        super(TestContactsAPI, self).__init__(methodName)

        # print self.app
        # print self.client


    def setUp(self):
        super(TestContactsAPI, self).setUp()
        self.url = url_for('contactapi0.contactapi')


    def api_call(self, method, data, path=''):
        #assert isinstance(self.client, flask.testing.FlaskClient)
        response = self.client.open(self.url + path, method=method, headers=self.headers, data=json.dumps(data))
        if response.status_code != 200:
            print response.status # code and title
        print response.data
        # response.data is text
        # response.json is decoded data
        return response

    def testInitialListIsEmpty(self):
        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.json['num_results'])

    def testCRUD(self):
        # Make a POST request to create an object in the database.
        user_email = 'john.doe@example.com'
        data = dict(first_name='John', last_name="Doe", emails=[dict(email=user_email)])
        print "* Create first user with email"
        response = self.api_call('POST', data)
        self.assertEquals(201, response.status_code)

        # The new record should be retrieved by list
        print "* Retrieve all contacts"
        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.json['num_results'])
        print "** email is ", response.json['objects'][0]['emails'][0]['email']
        self.assertEquals(user_email, response.json['objects'][0]['emails'][0]['email'])

        # The new record should be retrieved by id
        print "* Retrieve first contact"
        response = self.api_call('GET', None, path='/1')
        self.assertEquals(200, response.status_code)
        print "retrieved_contact =", response.json
        self.assertEquals(user_email, response.json['emails'][0]['email'])

        # update record
        new_email = 'john@doe.com'
        print "* Updating contact's email"
        data = dict(first_name='John', last_name="Doe", emails=[dict(email=new_email)])
        response = self.api_call('PATCH', data, path='/1')
        #response = self.api_call('PATCH', data)
        # FIXED AssertionError: Dependency rule tried to blank-out primary key column 'emails.contact_id' on instance '<Email at 0x404c810>'
        #       with Contact.email cascade="save-update, merge, delete, delete-orphan"
        self.assertEquals(200, response.status_code)
        self.assertEquals(new_email, response.json['emails'][0]['email'])

        # delete record
        print "* Deleting contact"
        response = self.api_call('DELETE', None, path='/1')
        self.assertEquals(204, response.status_code)

        print "* Retrieve all contacts"
        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.json['num_results'])

if __name__ == '__main__':
    unittest.main()