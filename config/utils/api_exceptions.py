from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class APIValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=status_code):
        super().__init__(detail, code)
        self.status_code = status_code


def uni_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    return response
