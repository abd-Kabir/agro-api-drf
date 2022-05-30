from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from config.utils.date_utils import date_transform
from config.utils.ordering_fields import ordering_guarantee_model
from config.utils.var_in_loop import get_guarantee_data
from apps.files_app.utils import upload_file
from apps.guarantee_agreem.filters import GuaranteeFilter
from apps.guarantee_agreem.models import GuaranteeAgreement
from apps.guarantee_agreem.serializer import GuaranteeListSerializer

import logging

logger = logging.getLogger()


class GuaranteeListAPIView(ListAPIView):
    queryset = GuaranteeAgreement.objects.all()
    serializer_class = GuaranteeListSerializer
    filter_class = GuaranteeFilter
    search_fields = ['id', 'guarantor', 'guarantors_signed_count', 'leasing_agreem__order_model__technique__name__name',
                     'leasing_agreem__order_model__technique__model', ]
    ordering_technique_fields = ['name__name', 'model', 'price', ]
    ordering_leasing_fields = ['leasing_num', 'leasing_date', 'contract_price', 'number_of_techs', 'lessor_sign',
                               'lessee_sign', 'guarantor_sign', ]
    ordering_order_fields = ['order_date', 'order_num', ]
    ordering_guarantee_fields = ['guarantor', 'guarantors_signed_count', ]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering_name = request.query_params.get('ordering')
        if ordering_name:
            queryset = ordering_guarantee_model(ordering_name, GuaranteeAgreement, queryset,
                                                self.ordering_technique_fields, self.ordering_order_fields,
                                                self.ordering_leasing_fields, self.ordering_guarantee_fields)

        response_list_1 = []
        response_list_2 = []
        for data in range(len(queryset)):
            guarantee_data = get_guarantee_data(queryset, data, 1)
            response_list_1.append(guarantee_data)
            formatted_leasing = response_list_1[data]['leasing']['leasing_date'].strftime('%d.%m.%Y')
            response_list_1[data]['leasing']['leasing_date'] = formatted_leasing
        for data in range(len(queryset)):
            leasing_data = get_guarantee_data(queryset, data, 2)
            response_list_2.append(leasing_data)
            formatted_order = response_list_2[data]['order']['order_date'].strftime('%d.%m.%Y')
            response_list_2[data]['order']['order_date'] = formatted_order

        total_response = {
            'guarantee_res_1': response_list_1,
            'guarantee_res_2': response_list_2
        }

        return Response(total_response)


class GuaranteeCreateAPIView(CreateAPIView):
    serializer_class = GuaranteeListSerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance: GuaranteeAgreement = serializer.save()

            if request.FILES.get('payment_solvency'):
                payment_solvency = upload_file(file=request.FILES.get('payment_solvency'), guarantee_id=instance)
                instance.payment_solvency_id = payment_solvency.id
            if request.FILES.get('financial_stability'):
                financial_stability = upload_file(file=request.FILES.get('financial_stability'), guarantee_id=instance)
                instance.financial_stability_id = financial_stability.id
            if request.FILES.get('business_plan'):
                business_plan = upload_file(file=request.FILES.get('business_plan'), guarantee_id=instance)
                instance.business_plan_id = business_plan.id
            if request.FILES.get('expert_opinion'):
                expert_opinion = upload_file(file=request.FILES.get('expert_opinion'), guarantee_id=instance)
                instance.expert_opinion_id = expert_opinion.id
            instance.save()
            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_guarantee-{instance.id}-id '
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
