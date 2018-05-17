from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('shop/', views.store_list, name='store_list'),
    path('shop/<slug:store>/', views.store_detail, name='store_detail'),
    path('coupon/', views.coupon_list, name='coupon_list'),
    path('deals/', views.deal_index, name='deal_index'),
    path('deal/<slug:deal>/', views.deal_detail, name='deal_detail'),
    path('deal/cat/<slug:category_slug>', views.deal_index, name='deals_by_category'),
    path('search_deals/', views.search_deal, name='search_deal'),
]