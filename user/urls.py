# user/urls.py
from django.conf.urls import url
from .views import CustomUserDetail


urlpatterns = [
    # {% url 'user:details' user.uuid %}
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=CustomUserDetail.as_view(),
        name='user-detail'
    ),
]
