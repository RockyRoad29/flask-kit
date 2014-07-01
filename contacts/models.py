from base.models import CRUDMixin
from ext import db


class Contact(CRUDMixin, db.Model):
    #__tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Text)
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    notes = db.Column(db.Text)

    def __init__(self, first_name=None, last_name=None, email=None):
        """

        :param first_name:
        :param last_name:
        :param email:
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
