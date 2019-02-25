from rest_framework import serializers

from chat.models import Chat, ChatMembership, Message
from user.serializers import CustomUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    user_uuid = serializers.ReadOnlyField(source='user.uuid')
    chat_uuid = serializers.ReadOnlyField(source='chat.uuid')
    from_current_user = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Message
        fields = ('uuid', 'chat_uuid', 'user_username', 'user_uuid', 'created', 'text', 'from_current_user')

    def get_from_current_user(self, message):
        if 'request' in self.context:
            return self.context['request'].user == message.user
        return None


class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('uuid', 'messages',)

    def get_messages(self, chat):
        qs = Message.objects.filter(chat=chat).order_by('-created')[0:10]
        serializer = MessageSerializer(instance=qs, many=True, context=self.context)
        return serializer.data


class ChatMembershipSerializer(serializers.HyperlinkedModelSerializer):
    chat = serializers.SerializerMethodField()
    other_user = CustomUserSerializer()

    class Meta:
        model = ChatMembership
        fields = ('chat', 'other_user')

    # We're using this instead of ChatSerializer() so that we can pass the context (which contains the current user)
    # down to ChatSerializer, and then down to MessageSerializer (which uses it for its 'from_current_user' field)
    def get_chat(self, obj):
        serializer = ChatSerializer(instance=obj.chat, context=self.context)
        return serializer.data
