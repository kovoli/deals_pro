from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Store, Coupon, Deal, Category
from deals_pro import helpers
from watson import search as watson
from django.db.models import F


def store_list(request):
    store_list = Store.objects.all().order_by('title')
    posts = helpers.pg_records(request, store_list, 42)

    return render(request, 'shop/store_list.html', {'posts': posts})


def store_detail(request, store):
    shop = get_object_or_404(Store, slug=store)
    object_lists = Coupon.objects.filter(expired__gt=timezone.now())
    coupons = object_lists.filter(shop_id=shop)
    deal_list = Deal.objects.all().filter(shop_id=shop).order_by('-publish')
    posts = helpers.pg_records(request, deal_list, 12)
    count_sum_deals = Deal.objects.filter(shop_id=shop).count()
    deals_count = count_sum_deals
    count_sum_coupons = coupons.count()

    return render(request, 'shop/store_detail.html', {'shop': shop,
                                                      'coupons': coupons,
                                                      'posts': posts,
                                                      'deals_count': deals_count,
                                                      'count_sum_coupons': count_sum_coupons})


def coupon_list(request):
    posts = Coupon.objects.filter(expired__gt=timezone.now())

    return render(request, 'coupon/coupons_list.html', {'posts': posts})


def deal_index(request, category_slug=None):
    deals = Deal.objects.all().order_by('-publish')
    posts = helpers.pg_records(request, deals, 12)

    category = None
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post_list = deals.filter(categoryId=category)
        posts = helpers.pg_records(request, post_list, 12)

    return render(request, 'deals/deals_list.html', {'posts': posts,
                                                     'category': category,
                                                     'categories': categories})


def deal_detail(request, deal):
    deal = get_object_or_404(Deal, slug=deal)
    deal.views = F('views') + 1
    deal.save()
    deal.refresh_from_db(fields=['views'])
    return render(request, 'deals/deal_detail.html', {'deal': deal})


def search_deal(request):
    if 'q' in request.GET:
        q = request.GET['q']
        search_results = watson.filter(Deal, q)
        posts = helpers.pg_records(request, search_results, 12)

        return render(request, 'deals/search_deals.html', {'posts': posts, 'q': q})
