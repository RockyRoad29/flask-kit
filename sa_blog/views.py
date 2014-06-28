from base.generic_views import DetailView, ListView, ModelViewMixin
from flask import url_for
from sa_blog import sa_blog
from sa_blog.forms import PostForm, CategoryForm
from sa_blog.models import Post, Category
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
    list_view = '.list'
    pass
#sa_blog.add_url_rule('/show/<id>', view_func = PostDetailView.as_view('detail'))
PostDetailView.map_to_url(sa_blog, '/show/<int:id>', 'detail')


class PostListView(PostBaseView, ListView):
    #template = 'Post_list.html'
    #list_fields = ['title', 'body']
    #list_fields = ['title', 'body','category']
    form_fields = ['title', 'body','category']
    detail_view = '.detail'
#sa_blog.add_url_rule('/list', view_func = PostListView.as_view('list'))
PostListView.map_to_url(sa_blog, '/list', 'list')


########################################################################################


class CategoryBaseView(ModelViewMixin):
    model = Category
    #list_fields = ['name']
    form = CategoryForm
    pass


class CategoryDetailView(CategoryBaseView, DetailView):
    #template = 'category_detail.html'
    pass
#sa_blog.add_url_rule('/cat/show/<id>', view_func = CategoryDetailView.as_view('cat_detail'))
CategoryDetailView.map_to_url(sa_blog, '/cat/show/<int:id>', 'cat_detail')


class CategoryListView(CategoryBaseView, ListView):
    #template = 'Category_list.html'
    detail_view = '.cat_detail'

#sa_blog.add_url_rule('/cat/list', view_func = CategoryListView.as_view('cat_list'))
CategoryListView.map_to_url(sa_blog, '/cat/list', 'cat_list')

