from copy import deepcopy
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from config.utils.var_in_loop import get_payment_table_data
from apps.payment_graph.models import PaymentGraph, PaymentTable
from apps.payment_graph.serializer import PaymentGraphFirstSerializer, PaymentGraphCreateSerializer, \
    PaymentTableSerializer


class PaymentListFirstAPIView(ListAPIView):
    queryset = PaymentGraph.objects.all()
    serializer_class = PaymentGraphFirstSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]


class PaymentTableRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentTableSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(PaymentTable.objects.filter(payment_graph=kwargs['pk']))
        serializer = self.get_serializer(queryset, many=True)
        data_list = deepcopy(serializer.data)
        data_count = PaymentTable.objects.filter(payment_graph=kwargs['pk']).count()
        for data in range(len(queryset)):
            act_date = data_list[data]['payment_graph']['act']['act_date']
            act_date = datetime.strptime(act_date, '%Y-%m-%d')
            act_date = act_date.strftime('%d.%m.%Y')
            date = data_list[data]['date']
            date = datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%d.%m.%Y')
            data_list[data]['payment_graph']['act']['act_date'] = act_date
            data_list[data]['date'] = date
        return Response({
            "message": "Successfully created",
            "data": data_list,
            "data_count": data_count,
            "status": status.HTTP_200_OK
        })


class PaymentGraphCreateAPIView(CreateAPIView):
    serializer_class = PaymentGraphCreateSerializer

    # filter_class = PaymentGraphFilter

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            get_payment_table_data(instance, 0)

            return Response({
                "message": "Payment graph successfully created",
                "payment_id": instance.id
            })
        return Response({
            "errors": serializer.errors
        })
