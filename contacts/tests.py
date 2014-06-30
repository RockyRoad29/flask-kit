from flask import url_for
from testing import KitTestCase


class ContactsTestCase(KitTestCase):
    """
    Put here utilities, not tests.

    """

    # def db_addEntity(self, name="Sample", description="This is a sample for testing"):
    #     "Adds a record directly to model and database"
    #     entity = Entity(name, description)
    #     entity.save()
    #     return entity

class TestYourBluePrintPages(ContactsTestCase):

    def test_index(self):
        """
        Tests the contacts index page success code.
        :return:
        """
        response = self.client.get(url_for('contacts.index'))
        self.assert200(response)