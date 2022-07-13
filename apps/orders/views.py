import logging
import requests
import json
from datetime import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.expert_assessment.models import ExpertAssessment
from apps.leasing_agreem.models import LeasingAgreement
from apps.regions.models import Province, District
from apps.tools.models import FarmerSTIR
from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_order_model
from config.utils.var_in_loop import get_order_data, get_order_company_province_data, get_order_company_district_data, \
    get_order_company_data
from apps.files_app.utils import upload_file
from apps.orders.filters import OrdersFilter
from apps.orders.models import Order
from apps.orders.serializer import OrderListSerializer, OrderCreateSerializer, OrderRetrieveSerializer

logger = logging.getLogger()


# --------------------- Farmer side ---------------------

class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    # permission_classes = [IsAuthenticated, ]
    filter_class = OrdersFilter
    search_fields = ['order_num', 'order_date', 'technique__name__name', 'technique__model']
    ordering_technique_fields = ['name', 'model', 'number_of_techs', 'price', 'yearly_leasing_percent', 'subsidy',
                                 'leasing_term', 'prepaid_percent', 'contract_price', ]
    ordering_order_fields = ['order_num', 'order_date']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_order_model(ordering_name, queryset, self.ordering_technique_fields,
                                            self.ordering_order_fields)
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


class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderRetrieveSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderCreateAPIView(CreateAPIView):
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

            farmer_instance = FarmerSTIR.objects.create(
                stir=request.data.get('stir'),
                full_name=request.data.get('full_name'),
                short_name=request.data.get('short_name'),
                business_type=request.data.get('business_type'),
                business_structure=request.data.get('business_structure'),
                legal_address=request.data.get('legal_address'),
                postcode=request.data.get('postcode'),
                home_address=request.data.get('home_address'),
                phone_number=request.data.get('phone_number'),
                bank_name=request.data.get('bank_name'),
                mfo=request.data.get('mfo'),
                payment_account=request.data.get('payment_account'),
                director=request.data.get('director'),
                director_number=request.data.get('director_number'),
                accountant=request.data.get('accountant'),
                accountant_number=request.data.get('accountant_number'))

            instance.farmer_stir = farmer_instance
            instance.save()
            expert_assessment_instance = ExpertAssessment.objects.create(is_active=True,
                                                                         order_model=instance)
            LeasingAgreement.objects.create(leasing_num='23/26',
                                            leasing_date=datetime.now().date(),
                                            contract_price=request.data.get('contract_price'),
                                            number_of_techs=request.data.get('number_of_techs'),
                                            is_active=True,
                                            expert_assessment=expert_assessment_instance)
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


# --------------------- Leasing Company side ---------------------

class OrderCompanyProvinceListAPIView(ListAPIView):
    queryset = Province.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_list = []
        for data in range(len(queryset)):
            i_data = get_order_company_province_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class OrderCompanyDistrictListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = District.objects.filter(region_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_order_company_district_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class OrderCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(district_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_order_company_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)
