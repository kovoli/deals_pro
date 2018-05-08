from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('shop/<slug:store>/', views.store_detail, name='store_detail')
]