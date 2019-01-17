# realtime/admin.py
from django.contrib import admin

from .fcm.models import UserRegistrationToken
from .websocket.models import UserWebSocketActivity


class UserRegistrationTokenAdmin(admin.ModelAdmin):
    model = UserRegistrationToken
    list_display = ['registration_token', 'user', 'created']


class UserWebSocketActivityAdmin(admin.ModelAdmin):
    model = UserWebSocketActivity
    list_display = ['user', 'active']


admin.site.register(UserRegistrationToken, UserRegistrationTokenAdmin)
admin.site.register(UserWebSocketActivity, UserWebSocketActivityAdmin)
