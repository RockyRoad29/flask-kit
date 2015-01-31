from base.generic_views import ModelViewMixin, DetailView, ListView
from contacts import contacts
from contacts.forms import ContactForm
from contacts.models import Contact
from flask import url_for, redirect


@contacts.route('/', methods=['GET', 'POST'])
def index():
    #return "Hello World"
    return redirect(url_for('.list'))

class ContactBaseView(ModelViewMixin):
    model = Contact
    list_fields = ['first_name', 'last_name']
    form = ContactForm
    pass


class ContactDetailView(ContactBaseView, DetailView):
    #template = 'contact_detail.html'
    list_view = '.list'


    def new_form(self, obj=None):
        form_instance = super(ContactDetailView, self).new_form(obj)
        form_instance.emails.append_entry()#data=dict(email='sample@example.com'))
        return form_instance

#contacts.add_url_rule('/show/<id>', view_func = ContactDetailView.as_view('detail'))
ContactDetailView.map_to_url(contacts, '/show/<int:id>', 'detail')


class ContactListView(ContactBaseView, ListView):
    #template = 'Contact_list.html'
    #form_fields = ['first_name', 'last_name']
    detail_view = '.detail'
#contacts.add_url_rule('/list', view_func = ContactListView.as_view('list'))
ContactListView.map_to_url(contacts, '/list', 'list')


