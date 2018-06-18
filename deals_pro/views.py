from blog.models import Post
from shop.models import Store, Deal, Coupon
from django.shortcuts import render


def main_page_list(request):
    blog_main_list = Post.objects.all().order_by('-publish')[:6]
    shop_main_list = Store.objects.all().order_by('title')[:10]
    deals_main_list = Deal.objects.all().order_by('-views').filter(categoryId=308)[:8]
    deals_main_list_two = Deal.objects.all().order_by('-views').filter(categoryId=112)[:8]
    coupons = Coupon.objects.all()
    content = {'blog_main_list': blog_main_list,
               'shop_main_list': shop_main_list,
               'deals_main_list': deals_main_list,
               'deals_main_list_two': deals_main_list_two,
               'coupons': coupons}

    return render(request, 'index.html', content)
