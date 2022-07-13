from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from apps.expert_assessment.models import ExpertAssessment
from apps.expert_assessment.serializer import ExpertAssessmentCreateSerializer
import logging

from apps.files_app.utils import upload_file
from apps.regions.models import Province, District
from config.utils.var_in_loop import get_order_company_province_data, get_order_company_district_data, \
    get_expert_a_company_data

logger = logging.getLogger()


class ExpertAssessmentCreateAPIView(CreateAPIView):
    serializer_class = ExpertAssessmentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance: ExpertAssessment = serializer.save()

            if request.FILES.get('payment_solvency_file'):
                payment_solvency_file = upload_file(file=request.FILES.get('payment_solvency_file'),
                                                    expert_assessment_id=instance)
                instance.payment_solvency_file_id = payment_solvency_file.id
            if request.FILES.get('financial_stability_file'):
                financial_stability_file = upload_file(file=request.FILES.get('financial_stability_file'),
                                                       expert_assessment_id=instance)
                instance.financial_stability_file_id = financial_stability_file.id
            if request.FILES.get('business_plan_file'):
                business_plan_file = upload_file(file=request.FILES.get('business_plan_file'),
                                                 expert_assessment_id=instance)
                instance.business_plan_file_id = business_plan_file.id
            if request.FILES.get('expert_opinion_file'):
                expert_opinion_file = upload_file(file=request.FILES.get('expert_opinion_file'),
                                                  expert_assessment_id=instance)
                instance.expert_opinion_file_id = expert_opinion_file.id
            instance.save()

            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_expert_assessment-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "expert_assessment_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        logger.debug(f'func_name: {str(self.get_view_name())}; leasing_creation_failed '
                     f'; user:{str(request.user)};')
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


# --------------------- Leasing Company side ---------------------

class ExpertAssessmentCompanyProvinceListAPIView(ListAPIView):
    queryset = Province.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_list = []
        for data in range(len(queryset)):
            i_data = get_order_company_province_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class ExpertAssessmentCompanyDistrictListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = District.objects.filter(region_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_order_company_district_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)


class ExpertAssessmentCompanyListAPIView(ListAPIView):
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        queryset = ExpertAssessment.objects.filter(order_model__district_id=kwargs.get('pk'))
        response_list = []
        for data in range(len(queryset)):
            i_data = get_expert_a_company_data(queryset, data)
            response_list.append(i_data)

        logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)};')
        return Response(response_list)
