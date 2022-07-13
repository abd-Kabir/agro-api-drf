from django.urls import path

from apps.acts.views import ActListAPIView, ActCreateAPIView, ActCompanyProvinceListAPIView, \
    ActContractCompanyListAPIView, ActCompanyDistrictListAPIView, ActCompanyListAPIView

app_name = 'act'
urlpatterns = [
    path('list/', ActListAPIView.as_view(), name='list'),
    path('list-company-province/', ActCompanyProvinceListAPIView.as_view(), name='list-province'),
    path('list-company-district/<int:pk>/', ActCompanyDistrictListAPIView.as_view(), name='list-district'),
    path('list-company-contract/<int:pk>/', ActContractCompanyListAPIView.as_view(), name='list-company'),
    path('list-company/<int:pk>/', ActCompanyListAPIView.as_view(), name='list-company'),
    path('create/', ActCreateAPIView.as_view(), name='create'),
]
