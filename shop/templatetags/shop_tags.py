from django import template

register = template.Library()


from shop.models import Category, Deal, Store
from django.db.models import Count


@register.inclusion_tag('sidebar/category_deals_widget.html')
def show_deal_category():
    show_cat = Category.objects.annotate(num_posts=Count('deal'))
    categories = Category.objects.all()
    return {'show_cat': show_cat, 'categories': categories}


@register.inclusion_tag('sidebar/lasts_deals_widget.html')
def show_last_deals(count=5):
    show_deals = Deal.objects.all()[:count]
    return {'show_deals': show_deals}


@register.inclusion_tag('sidebar/trending_stores_widget.html')
def trending_stores(count=5):
    show_shops = Store.objects.all()[:count]
    return {'show_shops': show_shops}