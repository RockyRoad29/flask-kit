import datetime
from flask import url_for
from sa_blog import Post
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


class SaBlogTestCase(KitTestCase):
    def db_addPost(self, title="Volatile test post", body="This post will live as long as the test", category=None):
        "Adds a post directly to model and database"
        post = Post(title=title, body=body, category=category)
        post.save()
        return post

    def db_addCategory(self, name="Sample Category"):
        "Adds a category directly to model and database"
        cat = Category(name=name)
        cat.save()
        return cat


class ViewsTests(SaBlogTestCase):
    ADD_FORM_HEADER = 'Add a new entry'
    FAILED='Validation failed'
    SUCCESS='Successfully added'

    def setUp(self):
        KitTestCase.setUp(self)
        self.list_url = url_for('sa_blog.list')
        self.detail_url = url_for('sa_blog.detail', id=1)

    def test_add_simple_post(self):
        """Simple post"""
        self.login()
        response = self.client.post(self.list_url,
                                    data={'title': "Volatile test post",
                                          'body': "This post will live as long as the test"},
                                    follow_redirects=True)
        self.assertContains(response,'form-errors.',0)

        # check post has been added
        messages = self.flash_messages(response)
        print messages
        self.assertTrue(self.SUCCESS in messages)
        post = Post.query.one()
        self.assertIsNotNone(post)
        self.assertEquals("Volatile test post", post.title)

    def test_add_post_with_category(self):
        """Add a post with category"""
        cat = self.db_addCategory("Testing")
        self.login()
        response = self.client.post(self.list_url,
                                    data={'title': "Volatile test post",
                                          'body': "This post will live as long as the test",
                                          'category': cat.id},
                                    follow_redirects=True)
        self.assertContains(response,'form-errors.',0)

        # check post has been added
        messages = self.flash_messages(response)
        print messages
        self.assertTrue(self.SUCCESS in messages)
        post = Post.query.one()
        self.assertIsNotNone(post)
        self.assertEquals(cat, post.category)


    def test_post_title_required(self):
        """Post title is required."""
        self.login()
        # Post title is required
        response = self.client.post(self.list_url,
                                    data={'title': "",
                                          'body': "This post has no title"},
                                    follow_redirects=False)
        self.assertContains(response,'This field is required.',1)

    def test_postupdate(self):
        post = self.db_addPost()
        self.assertEquals(1,post.id)
        self.assertTrue(isinstance(post,Post))
        self.login()
        response = self.client.post(self.detail_url,
                                    data={'title': "Edited test post title",
                                          'body': "This post will live as long as the test. And live it",
                                          'category': post.category_id},
                                    follow_redirects=True)
        self.assertContains(response,'form-errors.',0)
        self.assertEquals("Edited test post title", post.title)

    def test_pub_date_is_updated(self):
        """
        When editing a post, the creation date should be preserved,
        but the publication date should be updated.
        """
        now = datetime.datetime.utcnow()
        #self.fail("Not implemented. Need an update view")
        post = self.db_addPost()
        self.assertEquals(1,post.id)
        # Make the post old
        d1 = datetime.datetime(2000, 1, 1)
        post.pub_date = d1
        post.save()

        post = Post.get_by_id(1)
        self.assertEquals(d1,post.pub_date)

        self.login()
        post_title = "Modified test post title"
        post_body = "This post will live as long as the test. And live it"
        response = self.client.post(self.detail_url,
                                    data={'title': post_title,
                                          'body': post_body,
                                          'category': post.category_id},
                                    follow_redirects=True)
        self.assertContains(response,'form-errors.',0)

        # Retrieve it again from db
        post = Post.get_by_id(1)
        self.assertEquals(post_title, post.title)
        print "Post date is now: %r" % post.pub_date
        self.assertTrue(post.pub_date > d1)
        print "  that is ", post.pub_date - now, " after this test begun"
        self.assertTrue(post.pub_date > now)


