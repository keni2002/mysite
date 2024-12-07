# Creating a simple template tag
from django import template
from ..models import Post
register = template.Library()
@register.simple_tag
def total_posts():
    return Post.objects.count()
#Django will use the function’s name as the tag name

#Creating an inclusion template tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}