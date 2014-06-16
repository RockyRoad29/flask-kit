# -*- coding: utf-8 -*-

"""
    Example additional blueprint.

    :copyright: \(c) 2014 by Michelle Baert.
    :license: BSD, see LICENSE for more details.
"""
from flask import url_for, flash
from flask.ext.login import current_user
from werkzeug.utils import redirect

from flask.templating import render_template
from flaskr import flaskr
from flaskr.models import Entry
from flaskr.forms import EntryForm

@flaskr.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('.show_entries'))

#@flaskr.route('/')
@flaskr.route('/entries', methods=['GET', 'POST'])
def show_entries():
    if current_user.is_authenticated():
        entry = Entry()
        form = EntryForm(obj=entry,csrf_enabled=True)
        if form.validate_on_submit():
            form.populate_obj(entry)
            entry.save()
            flash("Added entry")
            return redirect(url_for('.show_entries'))
    else:
        form = None

    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries, add_form=form)

