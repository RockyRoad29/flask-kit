from base.generic_views import DetailView, ListView, ModelViewMixin
from flask import url_for
from sa_blog import sa_blog
from sa_blog.forms import PostForm
from sa_blog.models import Post
from werkzeug.utils import redirect


@sa_blog.route('/', methods=['GET', 'POST'])
def index():
   return redirect(url_for('.list'))

class PostBaseView(ModelViewMixin):
    model = Post
    list_fields = ['title', 'body','category', 'pub_date']
    form = PostForm
    pass


class PostDetailView(PostBaseView, DetailView):
    #template = 'post_detail.html'
    pass
sa_blog.add_url_rule('/show/<id>', view_func = PostDetailView.as_view('detail'))


class PostListView(PostBaseView, ListView):
    #template = 'Post_list.html'
    #list_fields = ['title', 'body']
    #list_fields = ['title', 'body','category']
    form_fields = ['title', 'body','category']
    detail_view = '.detail'

sa_blog.add_url_rule('/list', view_func = PostListView.as_view('list'))
