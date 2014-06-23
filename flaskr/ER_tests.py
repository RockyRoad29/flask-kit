#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: {}
"""
A great python script.
"""
from base.models import CRUDMixin
from flask.ext.sqlalchemy import Model
from flaskr.models import Entry, Category
from testing import KitTestCase

__author__ = 'rockyroad'


class ER_Tests(KitTestCase):
    def test_models(self):
        py = Category(name='Python')
        #py = Category()
        #py.populate(name='Python')

        p = Entry(title='Hello Python!', text='Python is pretty cool', category=py)
        #db.session.add(py)
        #db.session.add(p)
        py.save()
        p.save()

        print dir(py)
        posts = py.posts.all()
        self.assertEquals(1,len(posts))
        self.assertEquals(p,posts[1])