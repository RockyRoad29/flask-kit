import sqlalchemy
from sa_blog.models import Category, Post
from testing import KitTestCase


class ER_Tests(KitTestCase):
    def test_models(self):
        """
        The `Quickstart <http://pythonhosted.org/Flask-SQLAlchemy/quickstart.html#simple-relationships>`_ test
        :return:
        """
        py = Category('Python')
        p = Post('Hello Python!', 'Python is pretty cool', py)
        py.save()
        p.save()
        self.assertEquals("<class 'sqlalchemy.orm.dynamic.AppenderBaseQuery'>", repr(type(py.posts)))
        posts = py.posts.all()
        self.assertEquals(1,len(posts))
        self.assertEquals(p,posts[0])