#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: {}
"""
Form source code generator
"""
from importlib import import_module
import json
from pprint import pprint
from base import User
from ext import db
from flask import current_app
from flask.ext.sqlalchemy import Model
from flask.ext.wtf import Form
from scripts.gen_imports import ImportsGenerator
from sqlalchemy.ext.declarative import DeclarativeMeta
import wtforms
from wtforms.ext.csrf.fields import CSRFTokenField
from wtforms.ext.sqlalchemy.orm import model_form
import yaml
from wtforms.ext.sqlalchemy.validators import Unique
__author__ = 'rockyroad'


class FormModuleGenerator():
    def __init__(self, package_name):
        self.models = self.find_models(package_name)
        current_app.logger.debug('Package: %s : found %d models', package_name, len(self.models))
        self.imports = ImportsGenerator()
        self.forms = []
        pprint(FormGenerator.samples)
        assert(wtforms.validators.Required in FormGenerator.samples)

    def add_form(self, meta):
        current_app.logger.debug('Examining metaform: %r', meta)
        gen = FormGenerator(meta, parent=self)
        code = gen.to_source()
        self.forms.append(code)

    def add_import(self, the_class):
        self.imports.add_class(the_class)

    def to_source(self):
        #file_header
        code = """
# -*- coding: utf-8 -*-
# Generated by RockyRoad's form_generator
#
# Ok, it still will need some correction, e.g. for lambdas,
# but it should be a good start.
#
# If the result doesn't fit what you expect,
# it might means that you should adjust your model definition.
"""
        code += self.imports.python()
        for form_code in self.forms:
            code += form_code
        return code

    @staticmethod
    def find_models(package_name):
        module = import_module(package_name + '.models')
        models = []
        for n, v in vars(module).iteritems():
            #current_app.logger.debug('Examining variable %s: %r', n, v)
            #if issubclass(v, db.Model):
            if isinstance(v, DeclarativeMeta):
                models.append(v)
        return models

    def gen_all(self):
        for model in self.models:
            current_app.logger.debug('Processing model: %r', model)
            meta = model_form(model, db_session=db, base_class=Form)
            self.add_form(meta)
        return self.to_source()


class FormGenerator():
    """
    Inspects a generated form and suggests code
    """
    #: Defining sample instances to filter out default values
    # TODO Ideally refer to a specifically designed model.
    #      Can't define it here because it has to be registered before use.
    my_form = model_form(User)
    samples = {v.__class__: v for v in [
               # Fields
               # can't be created outside of a model
               # all I get is wtforms.fields.core.UnboundField
               #wtforms.fields.simple.TextField(),
               #wtforms.fields.core.DateTimeField(),
               f for f in my_form()
               ] + [
               # Widgets
               wtforms.widgets.core.TextInput(),
               wtforms.widgets.core.Select(),
               wtforms.ext.sqlalchemy.fields.QuerySelectMultipleField(),
               # Validators
               wtforms.validators.Optional(),
               wtforms.validators.Required(),
               wtforms.validators.Length(max=0), # need an improbable value here
               #wtforms.ext.sqlalchemy.validators.Unique(),
               ]}
    def __init__(self, meta, parent=None):
        assert (isinstance(meta, wtforms.form.FormMeta))
        self.i_form = meta()
        self.members = []
        self.parent = parent

    def add_import(self, the_class):
        if self.parent:
            self.parent.add_import(the_class)
        if not (the_class in self.samples):
            current_app.logger.warning("No default values for %r", the_class)

    def add_member(self, fld, validators, widget, descr):
        self.members.append("    {0} = {1}({2!r}, validators={3}, widget={4}())".format(
            fld.name, fld.type, fld.label.text, validators, widget
        ))
        if descr:
            self.members.append(descr)
        self.members.append("\n")

    def field_properties(self, fld):
        """
        Filters a field object's dictionary to keep only relevant data
        """
        excludes = ('name', 'short_name', 'id', 'type', 'label', 'flags', 'validators')
        info = {k: v for k, v in fld.__dict__.iteritems() if v and k not in excludes}
        return info

    def describe_field(self, fld):
        info = self.field_properties(fld)
        if not info:
            return None
        try:
            text = yaml.dump(info, indent=2)
        except Exception as e:
            text = "ERROR: Yaml failed formating, json follows:\n"
            text += json.dumps(info, default=lambda o: {repr(o): repr(o.__dict__)}, indent=2, )
            current_app.logger.error("Yaml failed formating %s: %s", text, e)

        lines = text.split("\n")
        if lines[-1] == '':
            lines.pop()
        descr = "\n".join(['    # ' + line for line in lines])

        return descr

    def gen_constructor(self, v, excludes=[]):
        """
        Tries to build a constructor call to match provided instance.

        :param v: e.g. some Validator like in wtforms.ext.sqlalchemy.validators
        """
        args = {}
        c = v.__class__
        # FIXME Looping over class members omits some values,
        #       like Length.max.
        #       A solution would be to loop over instance members
        #       but then we get too much and clutter the output.
        # FIXME Instead of omitting empty values, we should omit
        #       values equal to their default...
        defaults = self.samples[c].__dict__ if c in self.samples else None
        if defaults:
            current_app.logger.debug('Got defaults for %r', c)
        for a in dir(v):
            if not a.startswith('_') and (a not in excludes):
                value = v.__getattribute__(a)
                if defaults:
                    if a in defaults and defaults[a]==value:
                        continue
                elif value is None:
                    continue
                args[a] = value
            else:
                pass
                # current_app.logger.debug("Omitting property %s.%s", c.__name__, a)
        arglist = ', '.join(["{0}={1!r}".format(a, args[a]) for a in args])
        return "{0}({1})".format(c.__name__, arglist)

    def inspect_fields(self):
        for fld in self.i_form:
            if isinstance(fld, CSRFTokenField):
                continue
            self.add_import(fld.__class__)
            validators = '['
            for v in fld.validators:
                self.add_import(v.__class__)
                validators += self.gen_constructor(v, excludes=['field_flags','string_check']) + ', '
            validators += ']'
            self.add_import(fld.widget.__class__)
            widget = self.gen_constructor(fld.widget, excludes=['input_type', 'html_params'])
            #descr = json.dumps(fld, default=lambda o: {repr(o): o.__dict__}, indent=4, )
            descr = self.describe_field(fld)
            self.add_member(fld, validators, widget, descr)

    def get_name(self):
        return self.i_form.__class__.__name__

    def to_source(self):
        self.inspect_fields()
        code = "\n\nclass %s(Form):\n" % (self.get_name())
        code += "\n".join(self.members)
        #code += "\n\n"

        return code


def form_from_model(model):
    from wtforms.ext.sqlalchemy.orm import model_form
    from flask.ext.wtf import Form

    meta = model_form(model, db_session=db, base_class=Form)
    return form_from_meta(meta)


def form_from_meta(meta):
    """

    :param meta: wtforms.form.FormMeta
    """
    inspector = FormGenerator(meta)
    return inspector.to_source()


def forms4package(package_name):
    import logging
    current_app.logger.setLevel(logging.DEBUG)
    gen = FormModuleGenerator(package_name)
    return gen.gen_all()

