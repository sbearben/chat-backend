# realtime/websocket/exceptions.py
import json

CLIENT_ERROR_NOT_FRIENDS = 0

CLIENT_ERROR_CHOICES = (
    (CLIENT_ERROR_NOT_FRIENDS, 'Users are not friends.'),
)


# This is just a general exception used by our websocket consumer to direct appropriate error responses to the client
class ChatClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    ERROR_CODE = 0
    ERROR_MESSAGE = "Client error."

    def __init__(self):
        self.type = "ERROR"
        self.error_code = self.ERROR_CODE
        self.error_message = self.ERROR_MESSAGE

    def instanceVariablesToDict(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(value)}

    def instanceVariablesToJsonString(self):
        return json.dumps(self.instanceVariablesToDict())


class NotFriendsError(ChatClientError):
    ERROR_CODE = 1
    ERROR_MESSAGE = "Users are not friends."

    def __init__(self, user_uuid):
        super().__init__()
        self.user_uuid = user_uuid


class UserNotLoggedInError(ChatClientError):
    ERROR_CODE = 2
    ERROR_MESSAGE = "You are not logged in."

    def __init__(self):
        super().__init__()
