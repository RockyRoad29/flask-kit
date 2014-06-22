# -*- coding: utf-8 -*-

"""
    Example additional blueprint.

    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""
from base.generic_views import DetailView, ListView, ModelViewMixin
from flask import url_for, flash
from flask.ext.login import current_user, login_required
from flask.views import MethodView
from werkzeug.utils import redirect

from flask.templating import render_template
from flaskr import flaskr
from flaskr.models import Entry
from flaskr.forms import EntryForm

@flaskr.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('.list'))

class EntriesView(MethodView):
    @flaskr.route('/entries')
    def get(self):

        entries = Entry.query.all()
        if current_user.is_authenticated():
            form = EntryForm()
        else:
           form = None
        # TODO rename 'show_entries' to 'entries' to match shorter url
        return render_template('show_entries.html', entries=entries, add_form=form)

    @flaskr.route('/entries')
    @login_required
    def post(self):
        """
        Adds a new entry

        :return:
        """
        entry = Entry()
        #entry = Entry.from_form_data(request.form)
        form = EntryForm(obj=entry)
        if form.validate_on_submit():
            form.populate_obj(entry)
            entry.save()
            flash("Added entry")
            return redirect(url_for('.show_entries'))
        else:
            flash("Invalid data")
        entries = Entry.query.all()
        return render_template('show_entries.html', entries=entries, add_form=form)

flaskr.add_url_rule('/entries/', view_func=EntriesView.as_view('show_entries'))


class EntryBaseView(ModelViewMixin):
    def __init__(self):
        self.model = Entry
        self.form = EntryForm


class EntryDetailView(EntryBaseView, DetailView):
    template = 'entry_detail.html'
    # Note: template 'base.detail.html' would override 'flaskr.detail.html'
    #       so we prefix filename to keep it in this blueprint.
    pass
flaskr.add_url_rule('/entry/<id>', view_func = EntryDetailView.as_view('entry'))


class EntryListView(EntryBaseView, ListView):
    #template = 'entry_list.html'
    list_fields = ['title', 'text']
    detail_view = '.entry' # endpoint for EntryDetailView
    pass

flaskr.add_url_rule('/entry_list', view_func = EntryListView.as_view('list'))
