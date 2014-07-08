from flask import url_for
from contacts.models import Contact, Email
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
        response = self.client.get(url_for('contacts.index'))
        self.assert200(response)

    def testJohnDoe(self):
        doe = self.db_addEntity("John", "Doe")

    def testEmail(self):
        """


        """
        doe = self.db_addEntity("John", "Doe")
        #: @type emails sqlalchemy.orm.Query
        emails = doe.emails
        self.assertEquals(0, emails.count())
        email = Email.create(email='john.doe@example.com', contact=doe)
        #doe.emails.append(email)
        self.assertEquals(1, emails.count())
        #self.assertEquals(email.id, emails.one().id)
        self.assertEquals(email.email, emails.one().email)
        Email.create(email='john.doe@hotmail.com', contact_id=doe.id)
        self.assertEquals(2, emails.count())
