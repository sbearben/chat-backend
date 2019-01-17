# user/serializers.py
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_url', read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('url', 'uuid', 'username', 'email')
