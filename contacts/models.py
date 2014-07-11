from base.models import CRUDMixin
from ext import db


class Contact(CRUDMixin, db.Model):
    #__tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    #email = db.Column(db.String(80), nullable=False)
    #: @type emails sqlalchemy.orm.Query
    phone = db.Column(db.Text)
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    notes = db.Column(db.Text)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # def set_email(self, email):
    #     if isinstance(Email, email):
    #         obj = email
    #     else:
    #         obj = Email.get_by_id(email)
    #         if not obj:
    #             obj = Email.create(email=email, contact_id = self.id)
    #     self.emails = obj
    #     return obj

class Email(CRUDMixin, db.Model):
    #__tablename__ = 'emails'
    email = db.Column(db.String(80), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(80), unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    # Relationship to Contact or any subtype instances
    contact = db.relationship('Contact', enable_typechecks=False,
                              backref=db.backref('emails', lazy='dynamic'),
    )

class Phone(CRUDMixin, db.Model):
    num = db.Column(db.String(25), primary_key=True)
    landline = db.Column(db.Boolean, nullable=True)
    work = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text, nullable=True)
    # contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    # contact = db.relationship('Contact', enable_typechecks=False,
    #                           backref=db.backref('phones', lazy='dynamic'),
