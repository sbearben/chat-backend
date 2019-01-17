# # realtime/fcm/urls.py
from django.conf.urls import url
from .views import RegistrationToken


urlpatterns = [
    # {% url 'fcm:token' %}
    url(
        regex=r'^token/$',
        view=RegistrationToken.as_view(),
        name='token-detail'
    ),
]