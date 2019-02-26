# chat/urls.py
from django.conf.urls import url

from chat import views as chat_views


urlpatterns = [
    url(
        regex=r'^chats/$',
        view=chat_views.ChatMembershipList.as_view(),
        name='chats-list'
    ),

    url(
        regex=r'^chats/(?P<uuid>[-\w]+)/$',
        view=chat_views.ChatDetails.as_view(),
        name='chat-detail'
    ),
]