from django import template

register = template.Library()

from blog.models import Post, Category, Tag
from shop.models import Deal, Store
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


@register.inclusion_tag('sidebar/lasts_deals_widget.html')
def show_last_deals(count=5):
    show_deals = Deal.objects.all()[:count]
    return {'show_deals': show_deals}


@register.inclusion_tag('sidebar/trending_stores_widget.html')
def trending_stores(count=5):
    show_shops = Store.objects.all()[:count]
    return {'show_shops': show_shops}




