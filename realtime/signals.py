# realtime/signals.py
from django.dispatch import receiver

from friendship.signals import friendship_request_created

from .messaging import send_created_friend_request


@receiver(friendship_request_created)
def friendship_created_callback(sender, **kwargs):
    send_created_friend_request(friend_request=sender)
