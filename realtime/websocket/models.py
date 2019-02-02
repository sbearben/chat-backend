# realtime/websocket/models.py
from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UserWebSocketActivity(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='uuid',
        primary_key=True)
    # group_name = models.CharField(max_length=64, null=True, default=None)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #if self.group_name == None:
            #self.group_name = construct_group_name_from_uuid(self.user.uuid)