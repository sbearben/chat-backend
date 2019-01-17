# friendships/exceptions.py
from rest_framework.exceptions import APIException


# This is a REST framework exception
class InvalidFriendRequest(APIException):
    status_code = 400
    detail = 'Invalid action - cannot send friend request'
    default_code = 'bad_request'
