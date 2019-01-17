# realtime/fcm/models.py
from django.db import models
from django.conf import settings

REGISTRATION_TOKEN_EMPTY = ""


class UserRegistrationTokenManager(models.Manager):

    def create_and_set_user_token(self, user, token):
        object, created = UserRegistrationToken.objects.get_or_create(user=user)
        object.registration_token = token
        object.save()

        return object

    def delete_user_token(self, user):
        try:
            UserRegistrationToken.objects.get(user=user).delete()
        except UserRegistrationToken.DoesNotExist:
            pass

    def get_token_if_exists(self, user):
        try:
            return UserRegistrationToken.objects.get(user=user).registration_token
        except UserRegistrationToken.DoesNotExist:
            return None


class UserRegistrationToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='uuid',
        primary_key=True)
    registration_token = models.CharField(max_length=250, null=False, default=REGISTRATION_TOKEN_EMPTY)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserRegistrationTokenManager()
