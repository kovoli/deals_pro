from blog.models import Post
from shop.models import Store, Coupon
from django.shortcuts import render
from datetime import datetime



def main_page_list(request):
    blog_main_list = Post.objects.all().order_by('-publish')[:6]
    shop_main_list = Store.objects.all().order_by('title')[:10]
    coupon_main_list = Coupon.objects.filter(expired__gt=datetime.now())[:10]

    content = {'blog_main_list': blog_main_list, 'shop_main_list': shop_main_list, 'coupon_main_list': coupon_main_list }

    return render(request, 'index.html', content)


