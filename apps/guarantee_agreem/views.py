import json

import requests
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from apps.regions.models import Province, District
from apps.tools.models import FarmerSTIR
from config.utils.ordering_fields import ordering_guarantee_model, ordering_guarantor_model
from config.utils.var_in_loop import get_guarantee_data, get_guarantor_data, get_guarantee_company_province_data, \
    get_guarantee_company_district_data, get_guarantee_company_data, get_guarantor_company_data
from apps.files_app.utils import upload_file
from apps.guarantee_agreem.filters import GuaranteeFilter
from apps.guarantee_agreem.models import GuaranteeAgreement, Guarantor
from apps.guarantee_agreem.serializer import GuarantorSerializer, GuaranteeSerializer

import logging

logger = logging.getLogger()


class GuaranteeListAPIView(ListAPIView):
    queryset = GuaranteeAgreement.objects.all()
    filter_class = GuaranteeFilter
    search_fields = ['id', 'guarantor__stir', 'leasing_agreem__order_model__technique__name__name',
                     'leasing_agreem__order_model__technique__model', ]
    ordering_technique_fields = ['name', 'model', 'price', ]
    ordering_leasing_fields = ['leasing_num', 'leasing_date', 'contract_price', 'number_of_techs', ]
    ordering_guarantee_fields = ['guarantor', 'lessor_sign', 'lessee_sign', 'guarantor_sign', ]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_guarantee_model(ordering_name, queryset, self.ordering_technique_fields,
                                                self.ordering_leasing_fields, self.ordering_guarantee_fields)

        response_list = []
        for data in range(len(queryset)):
            guarantee_data = get_guarantee_data(queryset, data)
            response_list.append(guarantee_data)
            formatted_leasing = response_list[data]['leasing']['leasing_date'].strftime('%d.%m.%Y')
            response_list[data]['leasing']['leasing_date'] = formatted_leasing

        return Response(response_list)


class GuarantorListAPIView(ListAPIView):
    search_fields = ['id', 'farmer_stir__full_name', 'farmer_stir__legal_address', 'farmer_stir__stir',
                     'farmer_stir__director', 'farmer_stir__phone_number', ]
    ordering_technique_fields = []
    ordering_leasing_fields = ['leasing_num', 'leasing_date', 'contract_price', 'number_of_techs', ]
    ordering_guarantor_fields = ['guarantee_agreem', ]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Guarantor.objects.filter(guarantee_agreem=kwargs['guarantee']))
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_guarantor_model(ordering_name, queryset, self.ordering_technique_fields,
                                                self.ordering_leasing_fields, self.ordering_guarantor_fields)
        guarantors_list = []
        response_list = {}
        if queryset:
            for data in range(len(queryset)):
                guarantee_data = get_guarantor_data(queryset, data)
                guarantors_list.append(guarantee_data)
                formatted_leasing = guarantors_list[data]['guarantee']['guarantee_date'].strftime('%d.%m.%Y')
                guarantors_list[data]['guarantee']['guarantee_date'] = formatted_leasing
            response_list['guarantors_count'] = queryset[
                0].guarantee_agreem.leasing_agreem.expert_assessment.guarantors_count
            response_list['data'] = guarantors_list

        return Response(response_list)


class GuarantorCreateAPIView(CreateAPIView):
    serializer_class = GuarantorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            guarantors_count = Guarantor.objects.filter(
                guarantee_agreem=serializer.validated_data['guarantee_agreem']).count()
            guarantors_limit = GuaranteeAgreement.objects.get(
                pk=int(request.data['guarantee_agreem'])).leasing_agreem.expert_assessment.guarantors_count
            # guarantors_limit = 10
            if guarantors_count < guarantors_limit:
                instance = serializer.save()

                if request.FILES.get('payment_solvency_file'):
                    payment_solvency_file = upload_file(file=request.FILES.get('payment_solvency_file'),
                                                        guarantor_id=instance)
                    instance.payment_solvency_file_id = payment_solvency_file.id
                if request.FILES.get('financial_stability_file'):
                    financial_stability_file = upload_file(file=request.FILES.get('financial_stability_file'),
                                                           guarantor_id=instance)
                    instance.financial_stability_file_id = financial_stability_file.id
                if request.FILES.get('business_plan_file'):
                    business_plan_file = upload_file(file=request.FILES.get('business_plan_file'),
                                                     guarantor_id=instance)
                    instance.business_plan_file_id = business_plan_file.id
                if request.FILES.get('expert_opinion_file'):
                    expert_opinion_file = upload_file(file=request.FILES.get('expert_opinion_file'),
                                                      guarantor_id=instance)
                    instance.expert_opinion_file_id = expert_opinion_file.id
                instance.save()

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

                logger.debug(f'func_name: {str(self.get_view_name())}; created_new_guarantor-{instance.id}-id '
                             f'; user:{str(request.user)};')
                return Response({
                    "message": "Successfully created",
                    "guarantor_id": instance.id,
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            else:
                logger.debug(f'func_name: {str(self.get_view_name())}; limit_of_guarantors_reached_for_guarantee-'
                             f'{request.data["guarantee_agreem"]}-id '
                             f'; user:{str(request.user)};')
                return Response({
                    "message": "Guarantors limit exceeded",
                    "status": status.HTTP_405_METHOD_NOT_ALLOWED,
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        logger.debug(f'func_name: {str(self.get_view_name())}; guarantor_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class GuaranteeCreateAPIView(CreateAPIView):
    serializer_class = GuaranteeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_guarantor-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "leasing_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        logger.debug(f'func_name: {str(self.get_view_name())}; guarantor_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


# --------------------- Leasing Company side ---------------------

class GuaranteeCompanyProvinceListAPIView(ListAPIView):
    queryset = Province.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_list = []
        for data in range(len(queryset)):
            i_data = get_guarantee_company_province_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class GuaranteeCompanyDistrictListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = District.objects.filter(region_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_guarantee_company_district_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class GuaranteeCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = GuaranteeAgreement.objects.filter(
            leasing_agreem__expert_assessment__order_model__district_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_guarantee_company_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class GuarantorCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = Guarantor.objects.filter(guarantee_agreem_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_guarantor_company_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)
