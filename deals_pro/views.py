from blog.models import Post
from shop.models import Store, Deal
from django.shortcuts import render


def main_page_list(request):
    blog_main_list = Post.objects.all().order_by('-publish')[:6]
    shop_main_list = Store.objects.all().order_by('title')[:10]
    deals_main_list = Deal.objects.all()[:12]
    content = {'blog_main_list': blog_main_list,
               'shop_main_list': shop_main_list,
               'deals_main_list': deals_main_list}

    return render(request, 'index.html', content)
