from django.urls import path

from apps.tools.views import CurrencyWeatherAPIView, AgroLeasingBranchAPIView

app_name = 'tool'
urlpatterns = [
    path('currency-weather/', CurrencyWeatherAPIView.as_view(), name="currency-weather"),
    path('agro-branches/', AgroLeasingBranchAPIView.as_view(), name="agro-branches"),
]
