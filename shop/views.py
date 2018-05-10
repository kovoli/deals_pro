from django.shortcuts import render, get_object_or_404
from .models import Store, Coupon
from deals_pro import helpers
from _datetime import datetime


def store_list(request):
    store_list = Store.objects.all().order_by('title')
    posts = helpers.pg_records(request, store_list, 6)

    return render(request, 'shop/store_list.html', {'posts': posts})


def store_detail(request, store):
    shop = get_object_or_404(Store, slug=store)

    return render(request, 'shop/store_detail.html', {'shop': shop})


def coupon_list(request):
    posts = Coupon.objects.filter(expired__gt=datetime.now())

    return render(request, 'coupon/coupons_list.html', {'posts': posts})
