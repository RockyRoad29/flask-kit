from base.models import CRUDMixin
from ext import db
from flask import render_template, request, flash, current_app
import flask
from flask.ext.login import current_user, login_required
from flask.ext.sqlalchemy import Model
from flask.views import MethodView
#from wtforms.ext.appengine.db import model_form
from helpers import method_decorator, breakpoint
from flask.ext.wtf import Form
from scripts.form_generator import form_from_meta
import wtforms
from wtforms.ext.sqlalchemy.orm import model_form, model_fields

__author__ = 'rockyroad'




class ModelViewMixin(object):
    #: Your `models.CRUDMixin` model class
    model = None
    form = None
    list_fields = None
    form_fields = None

    def check_model(self):
        if self.model is None:
            raise NotImplementedError('I don\'t have a model to work with')
        assert (issubclass(self.model, CRUDMixin))
        assert (issubclass(self.model, Model))
        # current_app.logger.info('model query is %r', self.model.query) # flask_sqlalchemy.BaseQuery

    def new_entity(self):
        current_app.logger.info('new %s instance', self.model.__name__)
        return self.model()

    def authorized(self, action='Create'):
        """
        :seealso: `flask.ext.login.login_required`
        """
        return current_user.is_authenticated()

    def get_form(self):
        """
        Retrieves the model's form class.

        If not yet defined, will generate it from model,
        using `wtforms.ext.sqlalchemy.orm.model_form`.

        Example customization::

            if not self.form:
                self.form = model_form(MyModel, Form, field_args = {
                    'name' : {
                        'validators' : [validators.Length(max=10)]
                    }
                })
            return self.form

        :return: a `wtforms.form.Form` class

        :See also: Automatically create a WTForms Form from model `<http://flask.pocoo.org/snippets/60/>`_
        """
        if not self.form:
            assert(issubclass(Form, wtforms.Form)) # requirement of model_form
            self.form = model_form(self.model, db_session=db, base_class=Form)
            current_app.logger.info('built automatic wtf form for %s: %s', self.model.__name__, self.form)
        else:
            current_app.logger.info('using custom form for %s: %s', self.model.__name__, self.form)
        assert(issubclass(self.form, flask.ext.wtf.Form)) # otherwise might miss hidden_tag
        return self.form

    def new_form(self, obj=None):
        """
        Creates  new model form instance.


        :param obj: usually `request.form`
        :return: a new `flask.ext.wtf.Form` instance
        """
        return self.get_form()(obj=obj)

    def get_all(self):
        self.check_model()
        current_app.logger.info('retrieving all from %s', self.model.__name__)
        return self.model.query.all()

    def get_by_id(self, id):
        self.check_model()
        current_app.logger.info('retrieving %s from %s', id, self.model.__name__)
        return self.model.query.get_or_404(id)

    def get_list_fields(self):
        if not self.list_fields:
            self.list_fields = self.model.get_fields()
            current_app.logger.info('built list_fields from model %s : %r', self.model.__name__, self.list_fields)
        return self.list_fields


class DetailView(MethodView, ModelViewMixin):
    template = 'detail.html'

    def get(self, id):
        form = self.new_form() if self.authorized() else None
        return render_template(self.template, data=self.get_by_id(id), form=form)

    @method_decorator(login_required)
    def post(self):
        form = self.new_form(request.form)
        obj = None
        if form.validate():
            obj = self.new_entity()
            form.populate_obj(obj)
            obj.save()
            flash('Successfully added')
        else:
            flash('Validation failed. Please correct you data.')
        current_app.logger.info('POST form processed')
        return render_template(self.template, data=obj, form=form )


class ListView(MethodView, ModelViewMixin):
    """
    Remember that blueprint templates can be easily overriden from the main app's templates,
    which are first-in-line in Flask's template searchpath.
    """
    template = 'list.html'
    detail_view = None

    def build_context(self):
        """
        The template context will be similar for get and post renderings.

        Let's be DRY and put common items here.
        :return:
        """
        return {
            'data':self.get_all(),
            'list_fields': self.get_list_fields(),
            'form_fields': self.form_fields,
            'detail_view':self.detail_view
        }
    def get(self):
        current_app.logger.info('ListView.get for %s %s', id, self.__class__.__name__)

        ctx = self.build_context()
        form = self.new_form() if self.authorized('Create') else None
        ctx['add_form'] = form
        return render_template(self.template, **ctx)

    @method_decorator(login_required)
    def post(self):
        current_app.logger.info('ListView.post for %s with %s', self.__class__.__name__, request.form)
        form = self.new_form(request.form)
        if form.validate_on_submit():
            obj = self.new_entity()
            form.populate_obj(obj)
            obj.save()
            flash('Successfully added')
        else:
            current_app.logger.info('Validation failed %r', form.errors)
            flash('Validation failed. Please correct you data.')
        current_app.logger.info('POST form processed')

        #return render_template(self.template, data=self.get_all(), list_fields=self.get_list_fields(), add_form=form)
        ctx = self.build_context()
        ctx['add_form'] = form
        return render_template(self.template, **ctx)




# Register the urls
#my_blueprint.add_url_rule('/', view_func = ListView.as_view('list'))
#my_blueprint.add_url_rule('/<name>/', view_func = DetailView.as_view('detail'))
