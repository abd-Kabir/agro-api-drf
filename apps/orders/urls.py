from django.urls import path

from apps.orders.views import OrderCreateAPIView, OrderListAPIView

app_name = 'orders'
urlpatterns = [
    path('list/', OrderListAPIView.as_view(), name='list'),
    path('create/', OrderCreateAPIView.as_view(), name='create')
]
