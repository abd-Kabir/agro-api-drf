import json
import requests
import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils.api_exceptions import APIValidation
from apps.tools.models import AgroLeasingBranch
from apps.tools.utils.currency_weather_tools import (currency, get_weather)

logger = logging.getLogger()


class CurrencyWeatherAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        try:
            rates = {'usd_uzs': currency('USD'),
                     'eur_uzs': currency('EUR'),
                     'rub_uzs': currency('RUB'),
                     'weather': get_weather()}
            logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)}; Successful;')
            return Response(rates)
        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)}; Failed;')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)


class FarmerSTIRAPIView(APIView):
    def get(self, request, stir):
        try:
            url = f"http://agroportal.track.uz/api/company/get-detail/{stir}/"
            headers = {'Authorization': 'Token ad6eae21ed560da8e68f8c4f9b118d5744373c2e'}
            resp = json.loads(requests.get(url=url, headers=headers).text)

            response_data = {
                'stir': stir,
                'full_name': resp.get('name'),
                'short_name': resp.get('company_data').get('name'),
                'business_type': resp.get('company_data').get('businessType'),
                'business_structure': resp.get('company_data').get('businessStructure'),
                'legal_address': resp.get('company_data').get('streetName'),
                'postcode': resp.get('company_data').get('postcode'),
                'home_address': resp.get('company_data').get('house'),
                'phone_number': None,
                'bank_name': resp.get('company_data').get('banks')[0].get('bankName'),
                'mfo': resp.get('company_data').get('banks')[0].get('mfo'),
                'payment_account': resp.get('company_data').get('banks')[0].get('paymentAccount'),
                'director': resp.get('company_data').get('director'),
                'director_number': resp.get('company_data').get('director_number'),
                'accountant': None,
                'accountant_number': None,
            }

            logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)}; Successful;')
            return Response(response_data)
        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)}; Failed;')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)


class AgroLeasingBranchAPIView(APIView):
    def get(self, request):
        try:
            agro_branches = list(AgroLeasingBranch.objects.values_list('name', 'id'))
            data = []
            for name, _id in agro_branches:
                data.append({
                    "label": name,
                    "value": _id
                })
            return Response({
                "message": "Agro leasing branches was sent.",
                "data": data,
                "status": status.HTTP_200_OK
            })
        except Exception as exc:
            logger.debug(f'func_name: {str(self.get_view_name())}; user:{str(request.user)}; Failed;')
            raise APIValidation(detail=exc, status_code=status.HTTP_400_BAD_REQUEST)
