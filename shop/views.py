from django.shortcuts import render, get_object_or_404
from .models import Store, Coupon
from deals_pro import helpers
from _datetime import datetime


def store_list(request):
    store_list = Store.objects.all().order_by('title')
    posts = helpers.pg_records(request, store_list, 42)

    return render(request, 'shop/store_list.html', {'posts': posts})


def store_detail(request, store):
    shop = get_object_or_404(Store, slug=store)
    object_lists = Coupon.objects.filter(expired__gt=datetime.now())
    posts = object_lists.filter(shop_id=shop)

    return render(request, 'shop/store_detail.html', {'shop': shop, 'posts': posts})


def coupon_list(request):
    posts = Coupon.objects.filter(expired__gt=datetime.now())

    return render(request, 'coupon/coupons_list.html', {'posts': posts})


