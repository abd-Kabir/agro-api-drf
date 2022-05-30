from django.urls import path

from apps.acts.views import ActListAPIView, ActCreateAPIView

app_name = 'act'
urlpatterns = [
    path('list/', ActListAPIView.as_view(), name='list'),
    path('create/', ActCreateAPIView.as_view(), name='create'),
]
