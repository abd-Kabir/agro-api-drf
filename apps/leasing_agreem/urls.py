from django.urls import path

from apps.leasing_agreem.views import LeasingCreateAPIView, LeasingListAPIView

app_name = 'leasing'
urlpatterns = [
    path('create/', LeasingCreateAPIView.as_view(), name='create'),
    path('list/', LeasingListAPIView.as_view(), name='list'),
]
