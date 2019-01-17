# user/views.py
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserDetail(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'uuid'
