"""
@note: If you subclass models, you might want to read:

  - https://bitbucket.org/zzzeek/sqlalchemy/issue/500
  - http://docs.sqlalchemy.org/en/latest/changelog/changelog_03.html#change-0.3.6-12

  especially if you get an error suggesting ``enable_typechecks=False``

  @note: about normalization:

    - http://www.barrywise.com/2008/01/database-normalization-and-design-techniques/

"""
from sqlalchemy import UniqueConstraint

from base.models import CRUDMixin
from ext import db


class Contact(CRUDMixin, db.Model):
    #__tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    #email = db.Column(db.String(80), nullable=False)
    #: @type emails sqlalchemy.orm.Query
    # many-to-many
    emails = db.relationship('Email', backref=db.backref('contact'),
                             cascade="save-update, merge, delete, delete-orphan")
    #phone = db.Column(db.Text)
    phones = db.relationship('Phone', backref=db.backref('contact'))
    # many-to-one
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = db.relationship('Address', backref=db.backref('contacts', lazy='dynamic'))
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
    """
    Emails can be associated with contacts with a many-to-many
    relationship.

    How to implement it depends on whether we want to add extra
    data in the association instances as well as, or instead of,
    the target email itself.

    Here we essentially need to know *if an email address is able to reach a person*.

    An address may be valid and alive by itself but never reach a person
    for some reason, including that the person doesn't have access to a computer
    to check her mailbox. Another use case would be if a couple used to share a
    mailbox, but later break up, the address may be able to reach only one of them.

    Also, we can assume that shared email addresses is not the prevailing case.t

    So, like an association object, we'll use a multiple fields primary key,
    but we don't need a *child* model.

    """
    __tablename__ = 'emails'

    # Composite primary key
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), primary_key=True)
    email = db.Column(db.String(80), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(80), unique=True)

    # Relationship field is now declared as Contact.emails backref .
    # contact = db.relationship('Contact', enable_typechecks=False,
    #                           backref=db.backref('emails', lazy='dynamic'),
    # )

    status = db.Column(db.Enum('active', 'suspended', 'error'), nullable=False, default='active')
    notes = db.Column(db.Text)

    def __str__(self):
        return "%s <%s>" % (self.contact, self.email)

class Phone(CRUDMixin, db.Model):
    __tablename__ = 'phones'
    # Composite primary key
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), primary_key=True)
    num = db.Column(db.String(25), primary_key=True)
    type = db.Column(db.Enum('landline', 'mobile'), nullable=True)
    work = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text, nullable=True)
    # contact = db.relationship('Contact', enable_typechecks=False,
    #                           backref=db.backref('phones', lazy='dynamic'),

class Address(CRUDMixin, db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    postcode = db.Column(db.String(5))
    town = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    __table_args__ = (UniqueConstraint('address', 'postcode', 'town'),)
