# # realtime/fcm/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserRegistrationToken

from common.exceptions import MissingRequiredField, InvalidField


# fcm/token
class RegistrationToken(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        self.check_object_permissions(request, None)

        token = request.data.get('token', None)
        if token is None:
            raise MissingRequiredField(missing_field="token")
        elif token == "":
            raise InvalidField(invalid_field="token")

        UserRegistrationToken.objects.create_and_set_user_token(request.user, token)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, None)

        UserRegistrationToken.objects.delete_user_token(request.user)
        return Response(status=status.HTTP_200_OK)
