# realtime/messaging.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .events import (AcceptedFriendRequestEvent, CreatedFriendRequestEvent, NewMessageEvent,
                     RejectedFriendRequestEvent, CanceledFriendRequestEvent)


channel_layer = get_channel_layer()


def send_accepted_friend_request(user, other_user, chat):
    _send_realtime_event_to_user(
        user=user,
        realtime_event=AcceptedFriendRequestEvent(
            chat_uuid=chat.uuid,
            acceptor_uuid=other_user.uuid,
            acceptor_email=other_user.email,
            acceptor_username=other_user.username,
        )
    )


def send_created_friend_request(friend_request):
    _send_realtime_event_to_user(
        user=friend_request.to_user,
        realtime_event=CreatedFriendRequestEvent(
            sender_uuid=friend_request.from_user.uuid,
            sender_email=friend_request.from_user.email,
            sender_username=friend_request.from_user.username,
            date=friend_request.created,
        )
    )


def send_rejected_friend_request(friend_request):
    _send_realtime_event_to_user(
        user=friend_request.from_user,
        realtime_event=RejectedFriendRequestEvent(
            rejector_uuid=friend_request.to_user.uuid,
            rejector_email=friend_request.to_user.email,
            rejector_username=friend_request.to_user.username,
        )
    )


def send_canceled_friend_request(friend_request):
    _send_realtime_event_to_user(
        user=friend_request.to_user,
        realtime_event=CanceledFriendRequestEvent(
            canceler_uuid=friend_request.from_user.uuid,
            canceler_email=friend_request.from_user.email,
            canceler_username=friend_request.from_user.username,
        )
    )


def send_new_message(message, other_user, from_current_user):
    _send_realtime_event_to_user(
        user=other_user,
        realtime_event=NewMessageEvent(
            uuid=message.uuid,
            chat_uuid=message.chat.uuid,
            sender_uuid=message.user.uuid,
            sender_username=message.user.username,
            date=message.created,
            message=message.text,
            from_current_user=from_current_user,
        )
    )


def _send_realtime_event_to_user(user, realtime_event):
    async_to_sync(channel_layer.send)(
        "realtime-event-sender",
        {
            'type': 'send_event',
            'user_uuid_str': str(user.uuid),
            'realtime_event_dict': realtime_event.properties_dict,
        }
    )
