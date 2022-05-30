from datetime import datetime
import logging

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_order_model
from config.utils.var_in_loop import get_order_data
from apps.files_app.utils import upload_file
from apps.orders.filters import OrdersFilter
from apps.orders.models import Order
from apps.orders.serializer import OrderListSerializer, OrderCreateSerializer

logger = logging.getLogger()


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    # permission_classes = [IsAuthenticated, ]
    filter_class = OrdersFilter
    search_fields = ['order_num', 'order_date', 'technique__name__name', 'technique__model']
    ordering_technique_fields = ['name__name', 'model', 'number_of_techs', 'price', 'yearly_leasing_percent', 'subsidy',
                                 'leasing_term', 'prepaid_percent', 'contract_price', ]
    ordering_order_fields = ['order_num', 'order_date']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_order_model(ordering_name, Order, queryset,
                                            self.ordering_technique_fields, self.ordering_order_fields)
        serializer = self.get_serializer(queryset, many=True)
        response_list = serializer.data

        for data in range(len(queryset)):
            tech_data = get_order_data(queryset, data)
            response_list[data]['technique'] = tech_data
            formatted = date_transform(response_list, data, 'order_date')
            response_list[data]['order_date'] = formatted

        page = self.paginate_queryset(response_list)
        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return self.get_paginated_response(page)


class OrderCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            if request.FILES.get('file1'):
                upload_file(file=request.FILES.get('file1'), order_id=instance)
            if request.FILES.get('file2'):
                upload_file(file=request.FILES.get('file2'), order_id=instance)
            if request.FILES.get('file3'):
                upload_file(file=request.FILES.get('file3'), order_id=instance)

            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_order-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "order_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        logger.debug(f'func_name: {str(self.get_view_name())}; order_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
