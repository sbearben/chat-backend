# realtime/websocket/consumers.py
import json, uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from friendships.utils import users_are_friends

from .utils import add_user_as_active_websocket, add_user_as_inactive_websocket, construct_group_name_from_uuid
from .exceptions import ChatClientError, NotFriendsError, UserNotLoggedInError


# 'await' is used to call asynchronous functions that perform I/O
# - NOTE: ALL channel_layer methods are asynchronous
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user object (provided by the TokenAuthMiddleware in mysite/routing.py)
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()

        # We're taking the approach of each user gets a group- so here we construct the group name out of user's uuid
        self.user_group_name = construct_group_name_from_uuid(self.user.uuid)

        # Join room group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name  # I believe 'channel_name' is a unique name given per Consumer instance
        )
        print("adding as active")
        await add_user_as_active_websocket(self.user)

        # If we do not call this method within connect() then the connection will be rejected and closed.
        await self.accept()

    async def disconnect(self, close_code):
        print("Consumer: disconnect")
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        await add_user_as_inactive_websocket(self.user)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Messages will have a "command" key we can switch on
        command = text_data_json.get("command", None) # CLIENT ensures that the JSON they send back has this key with a valid value
        try:
            if command == "send_message":
                await self.send_message(text_data_json)
        except ChatClientError as e:
            # Catch any errors and send it back to the client
            await self.send(text_data=e.instanceVariablesToJsonString())


    ##### Command helper methods called by receive()

    async def send_message(self, text_data_json):
        destination_user_uuid = text_data_json['receiver_uuid']

        if not self.user.is_authenticated:
            raise UserNotLoggedInError()

        if not await database_sync_to_async(users_are_friends)(self.user, uuid.UUID(destination_user_uuid)):
            raise NotFriendsError(destination_user_uuid)

        # destination_user_channel_name = await self.get_user_channel_name_from_map(destination_user_uuid)
        destination_group_name = construct_group_name_from_uuid( destination_user_uuid)

        # Send message to room group - an event has a special 'type' key corresponding to the name of the method that
        # should be invoked on consumers that receive the event.
        #if await check_if_group_is_active(self.channel_layer, destination_group_name):
        await self.channel_layer.group_send(
            destination_group_name,
            {
                'type': 'chat_message', # so that 'chat_message' method below will be invoked on receiving consumers
                'uuid': text_data_json['uuid'],
                'chat_uuid': text_data_json['chat_uuid'],
                'sender_uuid': text_data_json['sender_uuid'],
                'sender_username': text_data_json['sender_username'],
                'date': text_data_json['date'],
                'message': text_data_json['message']
            }
        )

    # The following is called by the CONSUMER to send the message to the CLIENT
    async def send_consumer_event_to_client(self, event):
        await self.send(text_data=json.dumps(event))

    # Receive chat_message from room group and send down to client(s)
    async def chat_message(self, event):
        await self.send_consumer_event_to_client(
            event=event
        )
        '''
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'text_message',
            'uuid': event['uuid'],
            'chat_uuid': event['chat_uuid'],
            'sender_uuid': event['sender_uuid'],
            'sender_username': event['sender_username'],
            'date': event['date'],
            'message': event['message']
        }))
        '''

    # Receive accepted_friend_request from room group and send down to client(s)
    async def accepted_friend_request(self, event):
        print("Consumer: accepted_friend_request")
        await self.send_consumer_event_to_client(
            event=event
        )

    # Receive created_friend_request from room group and send down to client(s)
    async def created_friend_request(self, event):
        print("Consumer: created_friend_request")
        print(event)
        await self.send_consumer_event_to_client(
            event=event
        )

    # Receive rejected_friend_request from room group and send down to client(s)
    async def rejected_friend_request(self, event):
        print("Consumer: rejected_friend_request")
        await self.send_consumer_event_to_client(
            event=event
        )

    # Receive canceled_friend_request from room group and send down to client(s)
    async def canceled_friend_request(self, event):
        print("Consumer: canceled_friend_request")
        await self.send_consumer_event_to_client(
            event=event
        )
