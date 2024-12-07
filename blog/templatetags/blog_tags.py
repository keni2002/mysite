# Creating a simple template tag
import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

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

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
