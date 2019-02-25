# mysite/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

from realtime.websocket.token_auth import TokenAuthMiddlewareStack
from realtime.websocket.routing import websocket_urlpatterns

from realtime import consumers


# This root routing configuration specifies that when a connection is made to the Channels
# development server, the ProtocolTypeRouter will first inspect the type of connection. If
# it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.
application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
    'channel': ChannelNameRouter({
        'realtime-event-sender': consumers.EventSenderConsumer,
    }),
})