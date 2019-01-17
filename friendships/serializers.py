# friendships/serializers.py
from rest_framework import serializers
from friendship.models import FriendshipRequest, Friend
from user.serializers import CustomUserSerializer


class SentFriendRequestSerializer(serializers.ModelSerializer):
    to_user = CustomUserSerializer()

    class Meta:
        model = FriendshipRequest
        fields = ('to_user',)

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        user_representation = representation.pop('to_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation


class ReceivedFriendRequestSerializer(serializers.ModelSerializer):
    from_user = CustomUserSerializer()

    class Meta:
        model = FriendshipRequest
        fields = ('from_user',)

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        user_representation = representation.pop('from_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation


class FriendSerializer(serializers.ModelSerializer):
    from_user = CustomUserSerializer()

    class Meta:
        model = Friend
        fields = ('from_user',)

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        user_representation = representation.pop('from_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation
