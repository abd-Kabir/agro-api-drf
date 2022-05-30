from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from apps.orders.models import Order


class OrdersFilter(FilterSet):
    name = CharFilter(field_name='technique__name__name', lookup_expr='iexact')
    model = CharFilter(field_name='technique__model', lookup_expr='iexact')

    class Meta:
        model = Order
        fields = ['order_num', 'order_date', ]
