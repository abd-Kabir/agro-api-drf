from django.urls import path

from apps.leasing_agreem.views import LeasingCreateAPIView, LeasingListAPIView, \
    LeasingAgreemCompanyProvinceListAPIView, LeasingAgreemCompanyListAPIView, LeasingAgreemCompanyDistrictListAPIView

app_name = 'leasing'
urlpatterns = [
    path('create/', LeasingCreateAPIView.as_view(), name='create'),
    path('list/', LeasingListAPIView.as_view(), name='list'),
    path('list-company-province/', LeasingAgreemCompanyProvinceListAPIView.as_view(), name='list-province'),
    path('list-company-district/<int:pk>/', LeasingAgreemCompanyDistrictListAPIView.as_view(), name='list-district'),
    path('list-company/<int:pk>/', LeasingAgreemCompanyListAPIView.as_view(), name='list-company'),
]
