from django.urls import path

from apps.orders.views import OrderCreateAPIView, OrderListAPIView, OrderRetrieveAPIView, \
    OrderCompanyProvinceListAPIView, OrderCompanyDistrictListAPIView, OrderCompanyListAPIView

app_name = 'orders'
urlpatterns = [
    path('list/', OrderListAPIView.as_view(), name='list'),
    path('list-company-province/', OrderCompanyProvinceListAPIView.as_view(), name='list-province'),
    path('list-company-district/<int:pk>/', OrderCompanyDistrictListAPIView.as_view(), name='list-district'),
    path('list-company/<int:pk>/', OrderCompanyListAPIView.as_view(), name='list-company'),
    path('retrieve/<int:pk>/', OrderRetrieveAPIView.as_view(), name='retrieve'),
    path('create/', OrderCreateAPIView.as_view(), name='create')
]
