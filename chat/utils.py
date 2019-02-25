# chat/utils.py
from .models import Chat, ChatMembership


def create_chat_and_memberships(from_user, to_user):
    new_chat = Chat.objects.create()

    m1 = ChatMembership(user=from_user, other_user=to_user, chat=new_chat)
    m1.save()
    m2 = ChatMembership(user=to_user, other_user=from_user, chat=new_chat)
    m2.save()

    return new_chat, m1, m2
