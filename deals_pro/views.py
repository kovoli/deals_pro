from blog.views import Post
from django.shortcuts import render


def main_page_list(request):
    blog_main_list = Post.objects.all().order_by('-publish')[:3]

    return render(request, 'index.html', {'blog_main_list': blog_main_list})
