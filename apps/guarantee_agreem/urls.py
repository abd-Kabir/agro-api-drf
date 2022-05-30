from django.urls import path

from apps.guarantee_agreem.views import GuaranteeListAPIView, GuaranteeCreateAPIView

app_name = 'guarantee'
urlpatterns = [
    path('list/', GuaranteeListAPIView.as_view(), name='list'),
    path('create/', GuaranteeCreateAPIView.as_view(), name='create'),
]
