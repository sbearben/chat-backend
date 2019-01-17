# realtime/websocket/messaging.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .utils import construct_group_name_from_uuid


def send_event_via_websocket_group_consumer(user, websocket_event):
    channel_layer = get_channel_layer()
    group_name = construct_group_name_from_uuid(user.uuid)

    async_to_sync(channel_layer.group_send)(
        group_name,
        websocket_event.properties_dict,
    )