from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.acts.filters import ActFilter
from apps.acts.models import Act
from apps.acts.serializer import ActListSerializer, ActCreateSerializer
from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_act_model


class ActListAPIView(ListAPIView):
    queryset = Act.objects.all()
    serializer_class = ActListSerializer
    filter_class = ActFilter
    search_fields = ['act_num', 'act_date', 'seller_sign', 'lessor_sign', 'lessee_sign', 'seller',
                     'detected_defects_header', 'detected_defects_info', 'quality_conclusion_header',
                     'quality_conclusion_info', 'leasing_agreem__order_model__technique__model',
                     'leasing_agreem__order_model__technique__name__name']
    ordering_technique_fields = ['name', 'model', 'price', 'prepaid_percent', 'prepaid_price', ]
    ordering_leasing_fields = ['number_of_techs', 'contract_price', ]
    ordering_act_fields = ['act_num', 'act_date', 'lessor_sign', 'lessee_sign', 'guarantor_sign', 'seller', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_act_model(ordering_name, Act, queryset, self.ordering_technique_fields,
                                          self.ordering_leasing_fields, self.ordering_act_fields)
        serializer = self.get_serializer(queryset, many=True)
        for data in range(len(serializer.data)):
            formatted = date_transform(serializer.data, data, 'act_date')
            serializer.data[data]['act_date'] = formatted
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class ActCreateAPIView(CreateAPIView):
    queryset = Act.objects.all()
    serializer_class = ActCreateSerializer
