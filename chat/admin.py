# chat/admin.py
from django.contrib import admin

from .models import Chat, ChatMembership


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['pk', 'uuid', 'created',]


class ChatMembershipAdmin(admin.ModelAdmin):
    model = ChatMembership
    list_display = ['chat', 'user', 'other_user']


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMembership, ChatMembershipAdmin)
