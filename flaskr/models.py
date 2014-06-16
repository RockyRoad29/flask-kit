# -*- coding: utf-8 -*-

"""
    the most common models for the whole project.

    .. rubrique: about "mixin" classes
        * http://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful
        * http://en.wikipedia.org/wiki/mixin

    :copyright: \(c) 2014 by Michelle Baert.
    :license: bsd, see license for more details.

"""
from base.models import CRUDMixin
from ext import db

class Entry(CRUDMixin, db.Model):
    __tablename__ = 'flaskr_entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    text = db.Column(db.String, nullable=False)

