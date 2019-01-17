from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.serializers import CustomUserSerializer


class TokenSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
