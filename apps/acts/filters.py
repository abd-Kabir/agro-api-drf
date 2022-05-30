from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from apps.acts.models import Act


class ActFilter(FilterSet):
    name = CharFilter(field_name='leasing_agreem__order_model__technique__name__name', lookup_expr='iexact')
    model = CharFilter(field_name='leasing_agreem__order_model__technique__model', lookup_expr='iexact')

    class Meta:
        model = Act
        fields = ['id', 'name', 'model', ]
