from django.urls import path

from apps.guarantee_agreem.views import GuaranteeListAPIView, GuarantorCreateAPIView, GuarantorListAPIView, \
    GuaranteeCreateAPIView, GuaranteeCompanyProvinceListAPIView, GuaranteeCompanyDistrictListAPIView, \
    GuaranteeCompanyListAPIView, GuarantorCompanyListAPIView

app_name = 'guarantee'
urlpatterns = [
    path('guarantee/list/', GuaranteeListAPIView.as_view(), name='list-guarantee'),
    path('<str:guarantee>/guarantor/list/', GuarantorListAPIView.as_view(), name='list-guarantor'),
    path('guarantor/create/', GuarantorCreateAPIView.as_view(), name='create-guarantor'),
    path('guarantee/create/', GuaranteeCreateAPIView.as_view(), name='create-guarantee'),
    path('guarantee/list-company-province/', GuaranteeCompanyProvinceListAPIView.as_view(), name='list-province'),
    path('guarantee/list-company-district/<int:pk>/', GuaranteeCompanyDistrictListAPIView.as_view(),
         name='list-district'),
    path('guarantee/list-company/<int:pk>/', GuaranteeCompanyListAPIView.as_view(), name='list-company'),
    path('guarantor/list-company/<int:pk>/', GuarantorCompanyListAPIView.as_view(), name='list-company-guarantor'),
]
