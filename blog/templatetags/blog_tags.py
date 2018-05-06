from django import template

register = template.Library()

from ..models import Post, Category, Tag
from django.db.models import Count


@register.inclusion_tag('blog/sidebar/latest_post.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/sidebar/category_widget.html')
def show_categorys():
    num_cat = Category.objects.annotate(num_posts=Count('post'))
    return {'num_cat': num_cat}


@register.inclusion_tag('blog/sidebar/tags_widget.html')
def show_tags():
    tags = Tag.objects.all()
    return {'tags': tags}