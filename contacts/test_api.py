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
        return response

    def testInitialListIsEmpty(self):
        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        # response.data is text
        print response.data
        # response.json is decoded data
        self.assertEquals(0, response.json['num_results'])

    def testCRUD(self):
        # Make a POST request to create an object in the database.
        data = dict(first_name='John', last_name="Doe", email='john.doe@example.com')
        response = self.api_call('POST', data)
        self.assertEquals(201, response.status_code)

        # The new record should be retrieved by list
        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.json['num_results'])
        self.assertEquals(data['email'], response.json['objects'][0]['email'])

        # The new record should be retrieved by id
        response = self.api_call('GET', None, path='/1')
        self.assertEquals(200, response.status_code)
        print "retrieved_contact =", response.data
        self.assertEquals(data['email'], response.json['email'])

        # update record
        new_email = 'john@doe.com'
        response = self.api_call('PATCH', dict(email=new_email), path='/1')
        self.assertEquals(200, response.status_code)
        print "updated_contact = ", response.data
        self.assertEquals(new_email, response.json['email'])

        # delete record
        response = self.api_call('DELETE', None, path='/1')
        self.assertEquals(204, response.status_code)

        response = self.api_call('GET', None)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.json['num_results'])

if __name__ == '__main__':
    unittest.main()