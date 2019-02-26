# realtime/websocket/consumers.py
import json, uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from friendships.utils import users_are_friends

from .utils import add_user_as_active_websocket, add_user_as_inactive_websocket, construct_group_name_from_uuid
from .exceptions import ChatClientError, NotFriendsError, UserNotLoggedInError


# - NOTE: ALL channel_layer methods are asynchronous
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user object (provided by the TokenAuthMiddleware in mysite/routing.py)
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()

        self.user_group_name = construct_group_name_from_uuid(self.user.uuid)

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name  # I believe 'channel_name' is a unique name given per Consumer instance
        )

        await add_user_as_active_websocket(self.user)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        await add_user_as_inactive_websocket(self.user)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        data_serialized = json.loads(text_data)

        # Messages will have a "command" key we can switch on
        command = data_serialized.get("command", None) # CLIENT ensures that the JSON they send back has this key with a valid value
        try:
            if command == "send_message":
                await self.send_message(data_serialized)
        except ChatClientError as e:
            # Catch any errors and send it back to the client
            await self.send(text_data=e.instanceVariablesToJsonString())


    ##### Command helper methods called by receive()

    async def send_message(self, data_serialized):
        destination_user_uuid = data_serialized['receiver_uuid']

        if not self.user.is_authenticated:
            raise UserNotLoggedInError()

        if not await database_sync_to_async(users_are_friends)(self.user, uuid.UUID(destination_user_uuid)):
            raise NotFriendsError(destination_user_uuid)

        destination_group_name = construct_group_name_from_uuid( destination_user_uuid)

        # Send message to room group - an event has a special 'type' key corresponding to the name of the method that
        # should be invoked on consumers that receive the event.
        await self.channel_layer.group_send(
            destination_group_name,
            {
                'type': 'chat_message',  # so that 'chat_message' method below will be invoked on receiving consumers
                'uuid': data_serialized['uuid'],
                'chat_uuid': data_serialized['chat_uuid'],
                'sender_uuid': data_serialized['sender_uuid'],
                'sender_username': data_serialized['sender_username'],
                'date': data_serialized['date'],
                'message': data_serialized['message']
            }
        )

    # Receive chat_message from room group and send down to client(s)
    async def chat_message(self, message):
        await self._send_consumer_event_to_client(
            event=message
        )

    # Receive accepted_friend_request from room group and send down to client(s)
    async def accepted_friend_request(self, message):
        print("Consumer: accepted_friend_request")
        await self._send_consumer_event_to_client(
            event=message
        )

    # Receive created_friend_request from room group and send down to client(s)
    async def created_friend_request(self, message):
        print("Consumer: created_friend_request")
        print(message)
        await self._send_consumer_event_to_client(
            event=message
        )

    # Receive rejected_friend_request from room group and send down to client(s)
    async def rejected_friend_request(self, message):
        print("Consumer: rejected_friend_request")
        await self._send_consumer_event_to_client(
            event=message
        )

    # Receive canceled_friend_request from room group and send down to client(s)
    async def canceled_friend_request(self, message):
        print("Consumer: canceled_friend_request")
        await self._send_consumer_event_to_client(
            event=message
        )

    # The following is called by the CONSUMER to send the message to the CLIENT
    async def _send_consumer_event_to_client(self, event):
        await self.send(text_data=json.dumps(event))
