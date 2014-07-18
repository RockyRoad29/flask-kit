from flask import url_for
import flask_sqlalchemy
from sqlalchemy import func
from contacts.models import Contact, Email, Address, Phone
from ext import db
from testing import KitTestCase
#import sqlalchemy as sa
import sqlalchemy.orm


class ContactsTestCase(KitTestCase):
    """
    Put here utilities, not tests.
ct
    """

    def db_addEntity(self, first_name="John", last_name="Doe"):
        "Adds a record directly to model and database"
        entity = Contact.create(first_name=first_name, last_name=last_name)
        return entity


class TestContactsPages(ContactsTestCase):
    def test_index(self):
        """
        Tests the contacts index page success code.
        :return:
        """
        print self.client
        response = self.client.get(url_for('contacts.index'), follow_redirects=True)
        self.assert200(response)

    def testJohnDoe(self):
        doe = self.db_addEntity("John", "Doe")


class TestContactsModel(ContactsTestCase):
    def testCollections(self):
        """
        Collections are either or type `sqlalchemy.orm.collections.InstrumentedList`,
        `sqlalchemy.orm.attributes.InstrumentedAttribute`
        or `sqlalchemy.orm.dynamic.AppenderBaseQuery` if dynamically loaded.

        """
        email_address = 'john.doe@example.com'
        doe = Contact(first_name="John", last_name="Doe", emails=[Email(email=email_address)])

        # dynamic load not needed here since we have few emails and often needed
        print "Contact.emails is a", type(doe.emails)
        assert isinstance(doe.emails, sqlalchemy.orm.collections.InstrumentedList)
        email = doe.emails[0]
        self.assertEquals(email_address, email.email)

        # dynamic load not needed for phones either
        print "Contact.phones is a", type(doe.phones)
        assert isinstance(doe.phones, sqlalchemy.orm.collections.InstrumentedList)
        self.assertEquals(doe, email.contact)

        # postal address is many-to-one, backref rarely used
        doe.address = Address(postcode='29200')
        print "Address.contacts is a", type(Address.contacts)
        #assert isinstance(Address.contacts, sqlalchemy.orm.dynamic.AppenderBaseQuery)
        assert isinstance(Address.contacts, sqlalchemy.orm.attributes.InstrumentedAttribute)

    def testOptionalAttributes(self):
        # Contact needs only a last name
        doe = Contact(last_name="Doe")
        # doesn't raise integrity error
        doe.save()


class TestContactsEmailModel(ContactsTestCase):
    def testMultipleEmails(self):
        """
        Each contact can have multiple emails
        """
        doe = self.db_addEntity("John", "Doe")
        # no email doesn't raise integrity error
        doe.save()

        #: @type emails sqlalchemy.orm.Query
        emails = doe.emails
        #self.assertEquals(0, emails.count()) # this would be for 'dynamic' relationship, which return queries
        self.assertEquals(0, len(emails)) # len is suitable for a list


        # email can be appended to contact's collection
        emails.append(Email(email='john.doe@example.com')) # append is ok for both queries and lists
        self.assertEquals(1, len(doe.emails))
        # or created directly
        email2 = Email(email='john.doe@hotmail.com', contact=doe)
        self.assertEquals(2, len(doe.emails))

        # ensure persistence is ok
        email2.save()
        doe.save()
        self.assertEquals(2, Email.query.count())

    def testEmailBelongToContact(self):
        email2 = Email(email='john.doe@hotmail.com')
        try:
            email2.save()
            self.fail('Integrity error expected')
        except sqlalchemy.exc.IntegrityError  as e:
            self.assertEquals('(IntegrityError) emails.contact_id may not be NULL',
                              e.message)

    def testSharedEmail(self):
        doe = Contact(first_name='John', last_name='Doe',
                      emails=[Email(email='john.doe@example.com'),
                              Email(email='john.doe@hotmail.com')])
        self.assertEquals(2, len(doe.emails))
        jane = Contact(first_name='Jane', last_name='Doe',
                       emails=[Email(email='john.doe@hotmail.com')])
        db.session.add_all([doe, jane])
        db.session.commit()

        # How many email associations do we have ?
        emails = Email.query.all()
        self.assertEquals(3, len(emails))
        # we have no Email.contacts relationship because this is not a real many-to-many relationship

        # Who is reading 'john.doe@hotmail.com' ?
        shared = Email.query.filter(Email.email == 'john.doe@hotmail.com')
        assert isinstance(shared, sqlalchemy.orm.Query)
        assert isinstance(shared, flask_sqlalchemy.BaseQuery)
        assert isinstance(shared.all(), list)

        self.assertEquals(2, shared.count())
        print type(shared.all())
        results = [email.contact for email in shared]
        print results
        self.assertTrue(jane in results)
        self.assertEquals(jane, shared.filter(Email.contact_id == jane.id).one().contact)


class TestContactsPhoneModel(ContactsTestCase):
    def testMultiplePhones(self):
        """
        Each contact can have multiple phone numbers
        """
        phone_num = '01 23 45 67 89'
        doe = Contact(first_name="John", last_name="Doe", phones=[Phone(num=phone_num)])
        doe.save()

        doe.phones.append(Phone(num='98 76 54 32 10'))
        self.assertEquals(2, len(doe.phones))

        # or created directly

        phone3 = Phone(num='54 32 98 76 10', contact=doe)
        self.assertEquals(3, len(doe.phones))

        # ensure persistence is ok
        phone3.save()
        doe.save()
        self.assertEquals(3, Phone.query.count())

    def testPhoneBelongToContact(self):
        phone = Phone(num='98 76 54 32 10')
        try:
            phone.save()
            self.fail('Integrity error expected')
        except sqlalchemy.exc.IntegrityError  as e:
            self.assertEquals('(IntegrityError) phones.contact_id may not be NULL',
                              e.message)

    def testSharedPhone(self):
        common_phone = '98 76 54 32 10'
        doe = Contact(first_name='John', last_name='Doe',
                      phones=[Phone(num=common_phone),
                              Phone(num='54 32 98 76 10')]
        )
        self.assertEquals(2, len(doe.phones))
        jane = Contact(first_name='Jane', last_name='Doe',
                       phones=[Phone(num='01 23 45 67 89'),
                               Phone(num=common_phone)])
        # save both in one commit
        db.session.add_all([doe, jane])
        db.session.commit()

        # How many phone associations do we have ?
        phones = Phone.query.all()
        self.assertEquals(4, len(phones))
        # we have no Email.contacts relationship because this is not a real many-to-many relationship

        # Who is answering common_phone ?
        shared = Phone.query.filter(Phone.num == common_phone).all()
        self.assertEquals(2, len(shared))
        self.assertEquals(set((doe, jane)), set([phone.contact for phone in shared]))

        # Grouping: Which phone numbers are shared ?
        # http://stackoverflow.com/questions/8274069/sqlalchemy-group-by-and-count
        shared = db.session.query(Phone.num, func.count('*')). \
            group_by(Phone.num). \
            having(func.count('*') > 1).all()
        self.assertEquals(1, len(shared))
        self.assertEquals(common_phone, shared[0].num)


class TestContactsAddressModel(ContactsTestCase):
    def testEachContactHasZeroOrOneAddress(self):
        print type(Contact.address)
        assert isinstance(Contact.address, sqlalchemy.orm.attributes.InstrumentedAttribute)
        doe = Contact(first_name='John', last_name='Doe',
                      address=Address(address='Somewhere in the world', town="The World")
        )
        doe.save()

    def testContactsMaySharePostalAddress(self):
        print type(Address.contacts)
        common_address = Address(address="Shared address", town="Belleville")

        doe = Contact(first_name='John', last_name='Doe',
                      address=common_address)
        jane = Contact(first_name='Jane', last_name='Doe',
                       address=common_address)
        db.session.add_all([doe, jane])
        db.session.commit()

    def testAddressMustBeUnique(self):
        address1 = Address(address="Shared address", postcode='12345', town='Belleville')
        address1.save()

        try:
            address2 = Address(address="Shared address", postcode='12345', town='Belleville')
            address2.save()
            self.fail('Integrity error expected')
        except sqlalchemy.exc.IntegrityError as e:
            print e.message
        except Exception as e:
            print e.message
        db.session.rollback()
        self.assertEquals(1, Address.query.count())
