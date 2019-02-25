from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from friendship.models import Friend, FriendshipRequest

from user.utils import get_user_object

from common.permissions import IsOwnerOrDenied
from common.exceptions import MissingRequiredQueryParameter

from chat.models import Chat
from chat.serializers import ChatMembershipSerializer

# TODO: Sending the realtime events is blocking inside Views - need a way to perform asynchronously
from realtime.messaging import (send_accepted_friend_request, send_rejected_friend_request,
                                send_created_friend_request, send_canceled_friend_request)

from .serializers import (SentFriendRequestSerializer, ReceivedFriendRequestSerializer, FriendSerializer)
from .exceptions import InvalidFriendRequest


# me/receivedfriendrequests
class ReceivedFriendRequests(APIView):

    serializer_class = ReceivedFriendRequestSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenied,)
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        return FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
            to_user=user, rejected__isnull=True).all()

    def get_object(self):
        username = self.request.query_params.get('username', None)
        if username is None:
            raise MissingRequiredQueryParameter(missing_query_param="username")

        queryset = self.get_queryset()

        obj = get_object_or_404(queryset, from_user__username=username)
        self.check_object_permissions(self.request, obj.to_user)
        return obj

    # Return list of received friend requests
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # Accept a friend request from the user passed in to the 'username' query parameter
    def post(self, request, *args, **kwargs):
        received_friend_request = self.get_object()
        received_friend_request.accept()

        chat, _, membership = Chat.objects._create_chat(
            received_friend_request.from_user,
            received_friend_request.to_user
        )

        # Send to the user who initially sent this friend request a notification via WS or FCM that it was accepted
        send_accepted_friend_request(
            user=received_friend_request.from_user,
            other_user=received_friend_request.to_user,
            chat=chat
        )

        serializer = ChatMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Created since we're creating a Friend

    # Reject a friend request from the user passed in to the 'username' query parameter
    def delete(self, request, *args, **kwargs):
        received_friend_request = self.get_object()
        received_friend_request.reject()

        send_rejected_friend_request(
            friend_request=received_friend_request
        )

        serializer = self.serializer_class(received_friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


# me/sentfriendrequests
class SentFriendRequests(APIView):

    serializer_class = SentFriendRequestSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenied,)
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        return FriendshipRequest.objects.select_related('from_user').filter(
            from_user=user, rejected__isnull=True).all()

    def get_object(self):
        queryset = self.get_queryset()

        username = self.request.query_params.get('username', None)

        obj = get_object_or_404(queryset, from_user__username=username)
        self.check_object_permissions(self.request, obj.from_user)
        return obj

    # Return list of sent friend requests
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # Send a new friend request to the user passed in to the 'username' query parameter
    def post(self, request, *args, **kwargs):
        other_user = get_user_object(username=self.request.query_params.get('username'))

        # Send a friend request from currentUser to otherUser
        try:
            friend_request = Friend.objects.add_friend(
                request.user,
                other_user)
        except Exception as e:
            raise InvalidFriendRequest(detail=str(e))

        # Send to the other user who's receiving this friend request a notification via WS or FCM of a new request
        send_created_friend_request(
            friend_request=friend_request,
        )

        serializer = self.serializer_class(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # Created since we're creating a FriendRequest

    # Cancel a sent friend request to the user passed in to the 'username' query parameter
    def delete(self, request, *args, **kwargs):
        sent_friend_request = self.get_object()
        sent_friend_request.cancel()

        send_canceled_friend_request(
            friend_request=sent_friend_request
        )

        serializer = self.serializer_class(sent_friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


# me/friends
class FriendsList(APIView):

    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenied,)
    lookup_field = 'uuid'

    def get_queryset(self):
        return Friend.objects.select_related('from_user', 'to_user').filter(to_user=self.request.user).all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
