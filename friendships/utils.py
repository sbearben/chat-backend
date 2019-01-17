# friendships/utils.py
from django.core.exceptions import ObjectDoesNotExist

from friendship.models import Friend
from user.models import CustomUser


def users_are_friends(current_user, other_user_uuid):
    try:
        other_user = CustomUser.objects.get(uuid=other_user_uuid)
        if Friend.objects.are_friends(current_user, other_user):
            return True
    except ObjectDoesNotExist:
        pass

    return False
