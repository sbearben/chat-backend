# users/models.py
import uuid as uuid_lib

from django.conf import settings
from django.db import models
from django.urls import reverse

from realtime.messaging import send_new_message

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ChatManager(models.Manager):

    def delete_chat(self, chat_uuid):
        Chat.objects.filter(uuid=chat_uuid).delete()

    def delete_chat(self, from_user, to_user):
        chat = self._get_chat_by_intersection(from_user, to_user)
        if chat is not None:
            chat.delete()

    def get_or_create_chat(self, from_user, to_user):
        if self.chat_exists(from_user, to_user):
            return self._get_chat_by_membership(from_user, to_user), False

        return self._create_chat(from_user, to_user)[0], True

    def chat_exists(self, from_user, to_user):
        return ChatMembership.objects.filter(user=from_user, other_user=to_user).exists()
        # try:
            # m1 = ChatMembership.objects.get(user=from_user, other_user=to_user)
            # return True
        # except ChatMembership.DoesNotExist:
            # return False

    def _get_chat_by_intersection(self, from_user, to_user):
        try:
            qs1 = Chat.objects.filter(users=from_user)
            qs2 = Chat.objects.filter(users=to_user)
            return qs1.intersection(qs2).first()
        except Chat.DoesNotExist:
            return None

    def _get_chat_by_membership(self, from_user, to_user):
        try:
            return ChatMembership.objects.select_related('chat').get(user=from_user, other_user=to_user).chat
        except Chat.DoesNotExist:
            return None

    def _create_chat(self, from_user, to_user):
        new_chat = Chat.objects.create()
        m1 = ChatMembership.objects.create(user=from_user, other_user=to_user, chat=new_chat)
        m2 = ChatMembership.objects.create(user=to_user, other_user=from_user, chat=new_chat)

        return new_chat, m1, m2

    def _get_chat_and_chat_memberships(self, from_user, to_user):
        try:
            m1 = ChatMembership.objects.select_related('chat').get(user=from_user, other_user=to_user)
            m2 = ChatMembership.objects.select_related('chat').get(user=from_user, other_user=to_user)
        except ChatMembership.DoesNotExist:
            return None

        return m1.chat, m1, m2


class Chat(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        unique=True)
    users = models.ManyToManyField(
        AUTH_USER_MODEL,
        through='ChatMembership',
        through_fields=('chat', 'user'),
    )
    created = models.DateTimeField(auto_now_add=True)

    objects = ChatManager()

    def get_absolute_url(self):
        return reverse("chat-detail", kwargs={"uuid": self.uuid})


class Message(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='uuid')

    # related_name'messages' is needed so that the Chat Serializer knows how to find the chat's messages (since Chat is
    # related through a ForeignKey and doesn't have a messages field
    # - IMPORTANT: each time we set 'related_name' it needs to be unique across the app
    #   see: https://docs.djangoproject.com/en/2.1/topics/db/models/#abstract-related-name
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, to_field='uuid')
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=512)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)  # Call to super().save() is what actually saves the object in the DB
        # TODO: uncomment call to super and delete manually setting message 'created' field
        import datetime
        self.created = datetime.datetime.now()


class ChatMembership(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        unique=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, to_field='uuid')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='uuid')
    other_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membership_other_user",
    )

    class Meta:
        unique_together = (("chat", "user"), ("user", "other_user"),)
        indexes = [
            models.Index(fields=['user', 'other_user']),
        ]



