from django.urls import path

from apps.tools.views import CurrencyWeatherAPIView, AgroLeasingBranchAPIView, FarmerSTIRAPIView

app_name = 'tool'
urlpatterns = [
    path('currency-weather/', CurrencyWeatherAPIView.as_view(), name="currency-weather"),
    path('agro-branches/', AgroLeasingBranchAPIView.as_view(), name="agro-branches"),
    path('get_farmer/<str:stir>/', FarmerSTIRAPIView.as_view(), name="get_farmer_by_stir"),
]
