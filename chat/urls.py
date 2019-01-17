# chat/urls.py
from django.conf.urls import url

from chat import views as chat_views


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

    # {% url 'me:chats' %}
    url(
        regex=r'^chats/$',
        view=chat_views.ChatMembershipList.as_view(),
        name='chats-list'
    ),

    # {% url 'me:chats' chat.uuid %}
    url(
        regex=r'^chats/(?P<uuid>[-\w]+)/$',
        view=chat_views.ChatDetails.as_view(),
        name='chat-detail'
    ),
]