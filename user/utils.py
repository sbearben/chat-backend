# user/messaging.py
from django.http import Http404
from .models import CustomUser


def get_user_object(**kwargs):
    try:
        return CustomUser.objects.get(**kwargs)
    except CustomUser.DoesNotExist:
        raise Http404
