# realtime/websocket/utils.py
from channels.db import database_sync_to_async
from .models import UserWebSocketActivity


# Group names may only contain letters, digits, hyphens, and periods. Therefore this example code will fail on
# room names that have other characters (so we would need proper validation to tighten this up).
def construct_group_name_from_uuid(uuid):
    return 'chat_%s' % str(uuid)


def _set_user_websocket_activity(user, active):
    obj, created = UserWebSocketActivity.objects.get_or_create(user=user)
    if obj.active != active:
        obj.active = active
        obj.save()

@database_sync_to_async
def add_user_as_active_websocket(user):
    _set_user_websocket_activity(user, True)


@database_sync_to_async
def add_user_as_inactive_websocket(user):
    _set_user_websocket_activity(user, False)


def check_if_websocket_is_active(user):
    obj, created = UserWebSocketActivity.objects.get_or_create(user=user)
    return obj.active
