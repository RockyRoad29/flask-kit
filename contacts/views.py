from contacts import contacts


@contacts.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World"
    #return redirect(url_for('.list'))
