from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from apps.leasing_agreem.models import LeasingAgreement


class LeasingFilter(FilterSet):
    name = CharFilter(field_name='order_model__technique__name__name', lookup_expr='iexact')
    model = CharFilter(field_name='order_model__technique__model', lookup_expr='iexact')

    class Meta:
        model = LeasingAgreement
        fields = ['id', 'leasing_num', 'leasing_date', 'contract_price', 'number_of_techs', ]
