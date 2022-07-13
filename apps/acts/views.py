import logging

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from apps.acts.filters import ActFilter
from apps.acts.models import Act
from apps.acts.serializer import ActListSerializer, ActCreateSerializer
from apps.regions.models import Province, District
from apps.tools.models import FarmerSTIR
from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_act_model
from config.utils.var_in_loop import get_act_company_district_data, get_act_company_province_data, \
    get_act_company_data_contract, get_act_company_data

logger = logging.getLogger()


class ActListAPIView(ListAPIView):
    queryset = Act.objects.all()
    serializer_class = ActListSerializer
    filter_class = ActFilter
    search_fields = ['act_num', 'act_date', 'seller_sign', 'lessor_sign', 'lessee_sign', 'seller',
                     'detected_defects_header', 'detected_defects_info', 'quality_conclusion_header',
                     'quality_conclusion_info', 'leasing_agreem__expert_assessment__order_model__technique__model',
                     'leasing_agreem__expert_assessment__order_model__technique__name__name']
    ordering_technique_fields = ['name', 'model', 'price', 'prepaid_percent', 'prepaid_price', ]
    ordering_leasing_fields = ['number_of_techs', 'contract_price', ]
    ordering_act_fields = ['act_num', 'act_date', 'lessor_sign', 'lessee_sign', 'guarantor_sign', 'seller', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_act_model(ordering_name, queryset, self.ordering_technique_fields,
                                          self.ordering_leasing_fields, self.ordering_act_fields)
        serializer = self.get_serializer(queryset, many=True)
        for data in range(len(serializer.data)):
            formatted = date_transform(serializer.data, data, 'act_date')
            serializer.data[data]['act_date'] = formatted
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class ActCreateAPIView(CreateAPIView):
    queryset = Act.objects.all()
    serializer_class = ActCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            seller_instance = FarmerSTIR.objects.create(
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
            instance.seller_stir = seller_instance
            instance.save()
            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_act-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "act_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        logger.debug(f'func_name: {str(self.get_view_name())}; act_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


# --------------------- Leasing Company side ---------------------

class ActCompanyProvinceListAPIView(ListAPIView):
    queryset = Province.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_list = []
        for data in range(len(queryset)):
            i_data = get_act_company_province_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class ActCompanyDistrictListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = District.objects.filter(region_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_act_company_district_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class ActContractCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = Act.objects.filter(leasing_agreem__expert_assessment__order_model__district_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_act_company_data_contract(queryset, data)
            response_list.append(i_data)

        # logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class ActCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = Act.objects.get(pk=kwargs.get('pk'))
        i_data = get_act_company_data(instance)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(i_data)
