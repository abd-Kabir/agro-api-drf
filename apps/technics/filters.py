from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from apps.technics.models import Technique


class TechniqueFilter(FilterSet):
    name = CharFilter(field_name='name__name', lookup_expr='iexact')
    type = CharFilter(field_name='type__name', lookup_expr='iexact')

    class Meta:
        model = Technique
        fields = ['model', 'manufacturer', 'country_name', 'leasing_term', 'prepaid_percent', 'prepaid_price',
                  'yearly_leasing_percent', 'subsidy', 'guarantors_num', 'guarantee_bail', 'insurance', ]
