# users/models.py
import uuid as uuid_lib

from django.conf import settings
from django.db import models
from django.urls import reverse

from realtime.messaging import send_new_message

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


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
    #last_modified = models.DateTimeField(blank=True)

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
        #super().save(*args, **kwargs)  # Call to super().save() is what actually saves the object in the DB

        chat_membership = ChatMembership.objects \
            .select_related('other_user') \
            .only('other_user') \
            .filter(user=self.user, chat=self.chat)\
            .get()

        other_user = chat_membership.other_user
        send_new_message(message=self, other_user=other_user)


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
        unique_together = (("chat", "user"), )



