from django.urls import path
from apps.payment_graph.views import PaymentTableRetrieveAPIView, PaymentGraphCreateAPIView, PaymentListFirstAPIView

app_name = 'payment_graph'
urlpatterns = [
    path('retrieve/<int:pk>/', PaymentTableRetrieveAPIView.as_view(), name='retrieve'),
    path('list/', PaymentListFirstAPIView.as_view(), name='list'),
    path('create/', PaymentGraphCreateAPIView.as_view(), name='create')
]
