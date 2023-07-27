from django.urls import path
from . import views


urlpatterns = [
    path('', views.market, name='market'),
    path('order_<int:pk>/', views.buyProducts, name='order')
]
