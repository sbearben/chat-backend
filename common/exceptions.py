# common/exceptions.py
from rest_framework.exceptions import APIException


class MissingRequiredField(APIException):
    status_code = 400
    default_code = 'bad_request'

    def __init__(self, missing_field=""):
        self.detail = "Request error - missing required field '" + missing_field + "'"


class MissingRequiredQueryParameter(APIException):
    status_code = 400
    default_code = 'bad_request'

    def __init__(self, missing_query_param=""):
        self.detail = "Request error - missing required query parameter '" + missing_query_param + "'"


class InvalidField(APIException):
    status_code = 400
    default_code = 'bad_request'

    def __init__(self, invalid_field=""):
        self.detail = "Request error - invalid field '" + invalid_field + "'"
