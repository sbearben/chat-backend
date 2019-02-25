# common/exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status


class MissingRequiredField(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'missing_required_field'

    def __init__(self, missing_field=""):
        self.detail = "Request error - missing required field '" + missing_field + "'"


class MissingRequiredQueryParameter(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'missing_required_query_parameter'

    def __init__(self, missing_query_param=""):
        self.detail = "Request error - missing required query parameter '" + missing_query_param + "'"


class InvalidField(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid_field'

    def __init__(self, invalid_field=""):
        self.detail = "Request error - invalid field '" + invalid_field + "'"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found'

    def __init__(self, object_not_found):
        self.detail = "Request error - couldn't find " + object_not_found
