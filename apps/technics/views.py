import logging
import os
from rest_framework import status
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView, )

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from config.utils.api_exceptions import APIValidation
from config.utils.ordering_fields import ordering_technique_model
from apps.files_app.models import File
from apps.files_app.utils import upload_file
from apps.leasing_agreem.models import LeasingAgreement
from apps.orders.models import Order
from apps.technics.filters import TechniqueFilter
from apps.technics.models import Technique, TechniqueType, TechniqueName
from apps.technics.serializer import (TechnicsCreateSerializer,
                                      TechnicsListSerializer,
                                      TechnicsUpdateSerializer, TechnicsNamesSerializer, TechnicsTypesSerializer,
                                      TechnicsCompanyListSerializer)

logger = logging.getLogger()


class TechnicsListAPIView(ListAPIView):
    queryset = Technique.objects.all()
    serializer_class = TechnicsListSerializer
    filter_class = TechniqueFilter
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
    # permission_classes = [IsAuthenticated, ]

    search_fields = ['type__name', 'name__name', 'model', 'manufacturer', 'country_name', 'leasing_term',
                     'prepaid_percent', 'prepaid_price', 'price', 'yearly_leasing_percent', 'subsidy', 'guarantors_num',
                     'guarantee_bail', 'insurance', ]
    ordering_fields = ['id', 'name__name', 'model', 'manufacturer', 'country_name', 'leasing_term',
                       'prepaid_percent', 'prepaid_price', 'price', 'yearly_leasing_percent', 'subsidy',
                       'guarantors_num', 'guarantee_bail', 'insurance', ]

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            ordering_name = request.query_params.get('ordering')
            if ordering_name:
                queryset = ordering_technique_model(ordering_name, Technique, queryset, self.ordering_fields)
            serializer = self.get_serializer(queryset, many=True)
            page = self.paginate_queryset(serializer.data)
            logger.debug(f'func_name: {str(self.get_view_name())};  user:{str(request.user)};')
            return self.get_paginated_response(page)

        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; something_went_wrong'
                         f'; user:{str(request.user)};')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)


class TechnicsCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = TechnicsCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates a models instance.
        Args:
            request: gets technic's data from request and saves (files, data)
            *args: no data used
            **kwargs: no data used

        Returns: returns JSON serialized data which messages about successfully created data or sends error

        """
        serializer: ModelSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            instance = serializer.save()

            tech_manual = upload_file(file=request.FILES.getlist('technique_manual')[0], tech_id=instance)
            tech_passport = upload_file(file=request.FILES.getlist('technique_passport')[0], tech_id=instance)

            instance.prepaid_price = serializer.data.get('price') * (serializer.data.get('prepaid_percent') / 100)
            instance.technique_passport_id = tech_passport.id
            instance.technique_manual_id = tech_manual.id
            instance.save()
            if request.data.get('dragDrop'):
                list_of_id = request.data.get('dragDrop').split(',')
                for file_id in list_of_id:
                    file_without_id = File.objects.filter(id=int(file_id))
                    file_without_id.update(technique_id=instance.id)
            if request.FILES.getlist('file'):
                for file in request.FILES.getlist('file'):
                    upload_file(file=file, tech_id=instance)

            logger.debug(f'func_name: {str(self.get_view_name())}; created_new_tech-{instance.id}-id '
                         f'; user:{str(request.user)};')
            return Response({
                "message": "Successfully created",
                "technique_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        else:
            logger.debug(f'func_name: {str(self.get_view_name())}; cannot_create_tech-{serializer.errors}'
                         f'; user:{str(request.user)};')
            raise APIValidation(detail=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class TechnicsUpdateAPIView(UpdateAPIView):
    queryset = Technique.objects.all()
    serializer_class = TechnicsUpdateSerializer

    # permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        """
        Updates a model instance.
        Args:
            request: gets technic's data from request and updates data
            *args: no data used
            **kwargs: no data used

        Returns: returns JSON serialized data which messages about successfully updated data or sends error

        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            result = {
                "message": "Successfully updated",
                "details": serializer.data,
                "status": 200,
            }
            logger.debug(f'func_name: {str(self.get_view_name())}; updating_tech-{kwargs["pk"]}-id'
                         f'; user:{str(request.user)};')
            return Response(result)
        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; update_failed-{exc.__doc__}'
                         f'; user:{str(request.user)};')
            raise APIValidation(detail=f"{exc.__doc__} - {exc.args}", status_code=status.HTTP_400_BAD_REQUEST)


class TechnicsDetailAPIView(RetrieveAPIView):
    queryset = Technique.objects.all()
    serializer_class = TechnicsListSerializer

    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        logger.debug(f'func_name: {str(self.get_view_name())}; retrieving_tech-{kwargs["pk"]}-id '
                     f'; user:{str(request.user)};')
        try:
            return super().get(request, *args, **kwargs)
        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; retrieve_failed-{exc}'
                         f'; user:{str(request.user)};')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)


class TechnicsDeleteAPIView(DestroyAPIView):
    queryset = Technique.objects.all()
    serializer_class = TechnicsUpdateSerializer

    # permission_classes = [IsAuthenticated, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        files = File.objects.filter(technique_id=kwargs['pk'])
        for file in files:
            os.remove(file.path)
        if os.path.isfile(instance.technique_passport.path):
            os.remove(instance.tex_passport.path)
        if os.path.isfile(instance.technique_manual.path):
            os.remove(instance.texnika_qollanma.path)

        self.perform_destroy(instance)
        logger.debug(f'func_name: {str(self.get_view_name())}; deleted_files_belong_tech-{kwargs["pk"]}-id '
                     f'; user:{str(request.user)};')
        return Response({
            "message": "Successfully deleted.",
            "status": status.HTTP_204_NO_CONTENT
        })


class TechnicsTypeInfoAPIView(APIView):
    def get(self, request):
        list_of_types = list(TechniqueType.objects.values_list('id', 'name'))
        data = []
        for _id, _type in list_of_types:
            data.append({
                'id': _id,
                'label': _type,
                'value': _type
            })

        return Response({
            "message": "List of technics types sent.",
            "data": data,
            "status": status.HTTP_200_OK
        })


class TechnicsNameInfoAPIView(APIView):
    def get(self, request):
        list_of_names = TechniqueName.objects.values_list('name', flat=True)
        data = [{
            'value': '',
            'label': 'Barchasi'
        }]
        for _type in list_of_names:
            data.append({
                'label': _type,
                'value': _type
            })
        if data:
            return Response({
                "message": "List of technics names sent.",
                "data": data,
                "status": status.HTTP_200_OK
            })
        return Response({
            "message": "No technics names found",
            "status": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)


class TechnicsNamePKInfoAPIView(APIView):
    def get(self, request, pk):
        list_of_names = list(TechniqueName.objects.filter(type=pk).values_list('id', 'name'))
        data = []
        for _id, _type in list_of_names:
            data.append({
                'id': _id,
                'label': _type,
                'value': _type
            })
        if data:
            return Response({
                "message": "Names of technics was sent.",
                "data": data,
                "status": status.HTTP_200_OK
            })
        return Response({
            "message": "No data found.",
            "status": status.HTTP_404_NOT_FOUND
        })


class TechnicsNameCreateAPIView(CreateAPIView):
    serializer_class = TechnicsNamesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "message": "TechniqueName successfully created",
                "order_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


class TechnicsTypeCreateAPIView(CreateAPIView):
    serializer_class = TechnicsTypesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "message": "TechniqueType successfully created",
                "order_id": instance.id,
                "status": status.HTTP_201_CREATED
            })
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


class TechnicsCompanyList(ListAPIView):
    queryset = Technique.objects.all()
    serializer_class = TechnicsCompanyListSerializer
    filter_class = TechniqueFilter

    search_fields = ['id', 'type', 'name', 'model', 'manufacturer', 'country_name', 'leasing_term', 'prepaid_percent',
                     'prepaid_price', 'price', 'yearly_leasing_percent', 'subsidy', 'guarantors_num', 'guarantee_bail',
                     'insurance', ]
    ordering_fields = ['id', 'type', 'name', 'model', 'manufacturer', 'country_name', 'leasing_term', 'prepaid_percent',
                       'prepaid_price', 'price', 'yearly_leasing_percent', 'subsidy', 'guarantors_num',
                       'guarantee_bail', 'insurance', ]

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            ordering_name = request.query_params.get('ordering')
            if ordering_name:
                queryset = ordering_technique_model(ordering_name, Technique, queryset, self.ordering_fields)
            serializer = self.get_serializer(queryset, many=True)

            for i in serializer.data:
                i['orders_count'] = Order.objects.filter(technique_id=i.get('id')).count()
                i['leasing_count'] = LeasingAgreement.objects.filter(order_model__technique_id=i.get('id')).count()

            page = self.paginate_queryset(serializer.data)
            logger.debug(f'func_name: {str(self.get_view_name())};  user:{str(request.user)};')
            return self.get_paginated_response(page)

        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; something_went_wrong'
                         f'; user:{str(request.user)};')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)
