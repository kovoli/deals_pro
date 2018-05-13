from django.shortcuts import render, get_object_or_404
from .models import Store, Coupon, Deal, Category
from deals_pro import helpers
from _datetime import datetime


def store_list(request):
    store_list = Store.objects.all().order_by('title')
    posts = helpers.pg_records(request, store_list, 42)

    return render(request, 'shop/store_list.html', {'posts': posts})


def store_detail(request, store):
    shop = get_object_or_404(Store, slug=store)
    object_lists = Coupon.objects.filter(expired__gt=datetime.now())
    coupons = object_lists.filter(shop_id=shop)
    posts = Deal.objects.all().filter(shop_id=shop)

    return render(request, 'shop/store_detail.html', {'shop': shop, 'coupons': coupons, 'posts': posts})


def coupon_list(request):
    posts = Coupon.objects.filter(expired__gt=datetime.now())

    return render(request, 'coupon/coupons_list.html', {'posts': posts})


def deal_index(request, category_slug=None):
    deals = Deal.objects.all()
    posts = helpers.pg_records(request, deals, 5)

    category = None
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post_list = deals.filter(categoryId=category)
        posts = helpers.pg_records(request, post_list, 10)

    return render(request, 'deals/deals_list.html', {'posts': posts,
                                                   'category': category,
                                                   'categories': categories})

def deal_detail(request, deal):
    deal = get_object_or_404(Deal, slug=deal)
    return render(request, 'deals/deal_detail.html', {'deal': deal})
