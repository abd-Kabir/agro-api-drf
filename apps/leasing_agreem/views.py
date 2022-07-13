import logging
from datetime import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from apps.guarantee_agreem.models import GuaranteeAgreement
from apps.regions.models import Province, District
from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_leasing_model
from config.utils.var_in_loop import get_leasing_data, get_leasing_company_province_data, \
    get_leasing_company_district_data, get_leasing_company_data
from apps.leasing_agreem.filters import LeasingFilter
from apps.leasing_agreem.models import LeasingAgreement
from apps.leasing_agreem.serializer import LeasingCreateSerializer, LeasingListSerializer

logger = logging.getLogger()


class LeasingListAPIView(ListAPIView):
    queryset = LeasingAgreement.objects.all()
    serializer_class = LeasingListSerializer
    filter_class = LeasingFilter
    search_fields = ['leasing_num', 'leasing_date', 'contract_price', 'number_of_techs',
                     'order_model__technique__name__name', 'order_model__technique__model',
                     'order_model__technique__type__name']
    ordering_technique_fields = ['name', 'model', 'price', 'yearly_leasing_percent', 'subsidy', 'leasing_term',
                                 'prepaid_percent', ]
    ordering_leasing_fields = ['leasing_num', 'leasing_date', 'contract_price', 'number_of_techs', ]
    ordering_order_fields = ['order_num', 'order_date', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_leasing_model(ordering_name, queryset, self.ordering_technique_fields,
                                              self.ordering_order_fields, self.ordering_leasing_fields)
        serializer = self.get_serializer(queryset, many=True)
        response_list = serializer.data

        for data in range(len(queryset)):
            leasing_data = get_leasing_data(queryset, data)
            response_list[data].update(leasing_data)
            formatted_leasing = date_transform(response_list, data, 'leasing_date')
            formatted_order = response_list[data]['order']['order_date'].strftime('%d.%m.%Y')
            response_list[data]['leasing_date'] = formatted_leasing
            response_list[data]['order']['order_date'] = formatted_order

        # page = ordering_related_fields_leasing(ordering_name, self.ordering_fields, self.ordering_order_fields,
        #                                        response_list, self.paginate_queryset)

        logger.debug(f'func_name: {str(self.get_view_name())};  user:{str(request.user)};')
        return self.get_paginated_response(self.paginate_queryset(response_list))


class LeasingCreateAPIView(CreateAPIView):
    serializer_class = LeasingCreateSerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # if request.FILES.get('file'):
            #     upload_file(file=request.FILES.get('file'), leasing_id=instance)

            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_leasing-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "leasing_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        logger.debug(f'func_name: {str(self.get_view_name())}; leasing_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


# --------------------- Leasing Company side ---------------------

class LeasingAgreemCompanyProvinceListAPIView(ListAPIView):
    queryset = Province.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_list = []
        for data in range(len(queryset)):
            i_data = get_leasing_company_province_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class LeasingAgreemCompanyDistrictListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = District.objects.filter(region_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_leasing_company_district_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class LeasingAgreemCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = LeasingAgreement.objects.filter(expert_assessment__order_model__district_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_leasing_company_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)
