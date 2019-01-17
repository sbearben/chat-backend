# realtime/fcm/serializers.py
from rest_framework import serializers

from user.serializers import CustomUserSerializer

from .models import UserRegistrationToken


class UserRegistrationTokenSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    registration_token = serializers.ReadOnlyField(source='registration_token')

    class Meta:
        model = UserRegistrationToken
        fields = ('user', 'registration_token')