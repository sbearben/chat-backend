# chat/views.py
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat, ChatMembership, Message
from chat.serializers import ChatMembershipSerializer, MessageSerializer

from realtime.messaging import send_new_message

from common.exceptions import MissingRequiredField


# me/chats
class ChatMembershipList(APIView):

    serializer_class = ChatMembershipSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return ChatMembership.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Context was apparently needed for generating hyperlinked relations (and also passing current user in request)
        # - see: https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context
        serializer = self.serializer_class(queryset, many=True, context={'request':request})
        return Response(serializer.data)


# me/chats/<uuid>
class ChatDetails(APIView):

    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Message.objects.filter(chat=self.get_object())
        before_date = self.request.query_params.get('created_before', None)

        if before_date is not None:
            queryset = queryset.filter(created__lte=before_date)
        return queryset

    def get_object(self):
        chat_uuid = self.kwargs['uuid']
        obj = get_object_or_404(Chat.objects.all(), uuid=chat_uuid)

        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        text = self.request.data.get('text', None)
        if text is None:
            raise MissingRequiredField(missing_field="text")

        new_message = Message(chat=self.get_object(), user=self.request.user, text=text)
        new_message.save()

        chat_membership = ChatMembership.objects \
            .select_related('other_user') \
            .only('other_user') \
            .filter(user=self.request.user, chat=new_message.chat) \
            .get()

        other_user = chat_membership.other_user
        send_new_message(message=new_message, other_user=other_user, from_current_user=False)

        # pass context so that MessageSerializer has access to the current request and user
        serializer = self.serializer_class(new_message, context={'request':request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
