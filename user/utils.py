# user/messaging.py
from common.exceptions import NotFound

from .models import CustomUser


def get_user_object(**kwargs):
    try:
        return CustomUser.objects.get(**kwargs)
    except CustomUser.DoesNotExist:
        raise NotFound("user")
