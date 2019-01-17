# realtime/messaging.py
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from .events import (AcceptedFriendRequestEvent, CreatedFriendRequestEvent, NewMessageEvent,
                     RejectedFriendRequestEvent, CanceledFriendRequestEvent)

from .websocket.utils import check_if_websocket_is_active, construct_group_name_from_uuid
from .websocket.messaging import send_event_via_websocket_group_consumer
from .fcm.messaging import send_event_via_fcm


def send_realtime_event_to_user(user, realtime_event):
    if check_if_websocket_is_active(user):
        print("Realtime: send_realtime_event_to_user - websocket branch")
        send_event_via_websocket_group_consumer(user, realtime_event)
    else:
        print("Realtime: send_realtime_event_to_user - firebase branch")
        send_event_via_fcm(user, realtime_event)


def send_accepted_friend_request(user, other_user, chat):
    send_realtime_event_to_user(
        user=user,
        realtime_event=AcceptedFriendRequestEvent(
            chat_uuid=chat.uuid,
            acceptor_uuid=other_user.uuid,
            acceptor_email=other_user.email,
            acceptor_username=other_user.username,
        )
    )


def send_created_friend_request(friend_request):
    send_realtime_event_to_user(
        user=friend_request.to_user,
        realtime_event=CreatedFriendRequestEvent(
            sender_uuid=friend_request.from_user.uuid,
            sender_email=friend_request.from_user.email,
            sender_username=friend_request.from_user.username,
            date=friend_request.created,
        )
    )


def send_rejected_friend_request(friend_request):
    send_realtime_event_to_user(
        user=friend_request.from_user,
        realtime_event=RejectedFriendRequestEvent(
            rejector_uuid=friend_request.to_user.uuid,
            rejector_email=friend_request.to_user.email,
            rejector_username=friend_request.to_user.username,
        )
    )


def send_canceled_friend_request(friend_request):
    send_realtime_event_to_user(
        user=friend_request.to_user,
        realtime_event=CanceledFriendRequestEvent(
            canceler_uuid=friend_request.from_user.uuid,
            canceler_email=friend_request.from_user.email,
            canceler_username=friend_request.from_user.username,
        )
    )


def send_new_message(message, other_user):
    import datetime
    send_realtime_event_to_user(
        user=other_user,
        realtime_event=NewMessageEvent(
            uuid=message.uuid,
            chat_uuid=message.chat.uuid,
            sender_uuid=message.user.uuid,
            sender_username=message.user.username,
            date=datetime.datetime.now(),  # message.created,
            message=message.text,
        )
    )

    '''
    channel_layer = get_channel_layer()
    group_name = construct_group_name_from_uuid(other_user.uuid)

    import datetime
    # if async_to_sync(check_if_group_is_active)(channel_layer, group_name):
    async_to_sync(channel_layer.group_send)(
        group_name,
        NewMessageEvent(
            uuid=message.uuid,
            chat_uuid=message.chat.uuid,
            sender_uuid=message.user.uuid,
            sender_username=message.user.username,
            date=datetime.datetime.now(),  # message.created,
            message=message.text,
        ).properties_dict
    )
    '''
