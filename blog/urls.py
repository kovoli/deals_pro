from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('<slug:post>', views.blog_detail, name='blog_detail'),
    path('category/<slug:category_slug>', views.blog_index, name='posts_by_category'),
    path('tag/<slug:tag_slug>', views.blog_index, name='posts_by_tag'),
    path('search/', views.search, name='search'),
]