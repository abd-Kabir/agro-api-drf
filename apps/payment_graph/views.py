from copy import deepcopy
from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.payment_graph.filters import PaymentGraphFilter
from config.utils.ordering_fields import ordering_payment_graph_model
from config.utils.var_in_loop import get_payment_table_data, get_payment_table_other_data
from apps.payment_graph.models import PaymentGraph, PaymentTable
from apps.payment_graph.serializer import PaymentGraphFirstSerializer, PaymentGraphCreateSerializer, \
    PaymentTableSerializer


class PaymentListFirstAPIView(ListAPIView):
    queryset = PaymentGraph.objects.all()
    serializer_class = PaymentGraphFirstSerializer
    filter_class = PaymentGraphFilter
    search_fields = ['act__leasing_agreem__number_of_techs', 'act__leasing_agreem__leasing_num',
                     'act__leasing_agreem__leasing_date', 'act__leasing_agreem__contract_price',
                     'act__leasing_agreem__expert_assessment__order_model__technique__name__name',
                     'act__leasing_agreem__expert_assessment__order_model__technique__model',
                     'act__leasing_agreem__expert_assessment__order_model__technique__price',
                     'act__leasing_agreem__expert_assessment__order_model__technique__prepaid_percent',
                     'act__leasing_agreem__expert_assessment__order_model__technique__prepaid_price', ]
    ordering_technique_fields = ['name', 'model', 'price', 'prepaid_percent', 'prepaid_price', ]
    ordering_leasing_fields = ['number_of_techs', 'contract_price', 'leasing_num', 'leasing_date', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_payment_graph_model(ordering_name, queryset, self.ordering_technique_fields,
                                                    self.ordering_leasing_fields)
        serializer = self.get_serializer(queryset, many=True)
        for data in range(len(serializer.data)):
            leasing_date = serializer.data[data]['act']['leasing_agreem']['leasing_date']
            leasing_date = datetime.strptime(leasing_date, '%Y-%m-%d')
            formatted = leasing_date.strftime('%d.%m.%Y')
            serializer.data[data]['act']['leasing_agreem']['leasing_date'] = formatted
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class PaymentTableRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentTableSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(PaymentTable.objects.filter(payment_graph=kwargs['pk']))
        serializer = self.get_serializer(queryset, many=True)
        data_list = deepcopy(serializer.data)
        other_data = get_payment_table_other_data(queryset)
        data_count = PaymentTable.objects.filter(payment_graph=kwargs['pk']).count()
        for data in range(len(queryset)):
            date = data_list[data]['date']
            date = datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%d.%m.%Y')
            data_list[data]['date'] = date
        act_date = other_data['act_date']
        act_date = act_date.strftime('%d.%m.%Y')
        other_data['act_date'] = act_date
        return Response({
            "data_count": data_count,
            "status": status.HTTP_200_OK,
            "data": other_data,
            "payment_data": data_list
        })


class PaymentGraphCreateAPIView(CreateAPIView):
    serializer_class = PaymentGraphCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            get_payment_table_data(instance)

            return Response({
                "message": "Payment graph successfully created",
                "payment_id": instance.id
            })
        return Response({
            "errors": serializer.errors
        })
