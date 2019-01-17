# mysite/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from realtime.websocket.token_auth import TokenAuthMiddlewareStack
import realtime.websocket.routing


# This root routing configuration specifies that when a connection is made to the Channels
# development server, the ProtocolTypeRouter will first inspect the type of connection. If
# it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(realtime.websocket.routing.websocket_urlpatterns)
    )
})