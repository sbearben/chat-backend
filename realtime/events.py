# realtime/events.py

WEBSOCKET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class AcceptedFriendRequestEvent:
    def __init__(self, chat_uuid, acceptor_uuid, acceptor_email, acceptor_username):
        self._type = "accepted_friend_request"
        self._chat_uuid = chat_uuid
        self._acceptor_uuid = acceptor_uuid
        self._acceptor_email = acceptor_email
        self._acceptor_username = acceptor_username

    @property
    def type(self):
        return self._type

    @property
    def chat_uuid(self):
        return str(self._chat_uuid)

    @property
    def acceptor_uuid(self):
        return str(self._acceptor_uuid)

    @property
    def acceptor_email(self):
        return self._acceptor_email

    @property
    def acceptor_username(self):
        return self._acceptor_username

    @property
    def properties_dict(self):
        return dict(
            type=self.type,
            chat_uuid=self.chat_uuid,
            acceptor_uuid=self.acceptor_uuid,
            acceptor_email=self.acceptor_email,
            acceptor_username = self.acceptor_username,
        )


class CreatedFriendRequestEvent:
    def __init__(self, sender_uuid, sender_email, sender_username, date):
        self._type = "created_friend_request"
        self._sender_uuid = sender_uuid
        self._sender_email = sender_email
        self._sender_username = sender_username
        self._date = date

    @property
    def type(self):
        return self._type

    @property
    def sender_uuid(self):
        return str(self._sender_uuid)

    @property
    def sender_email(self):
        return self._sender_email

    @property
    def sender_username(self):
        return self._sender_username

    @property
    def date(self):
        return self._date.strftime(WEBSOCKET_DATETIME_FORMAT)

    @property
    def properties_dict(self):
        return dict(
            type=self.type,
            sender_uuid=self.sender_uuid,
            sender_email=self.sender_email,
            sender_username=self.sender_username,
            date=self.date,
        )


class RejectedFriendRequestEvent:
    def __init__(self, rejector_uuid, rejector_email, rejector_username):
        self._type = "rejected_friend_request"
        self._rejector_uuid = rejector_uuid
        self._rejector_email = rejector_email
        self._rejector_username = rejector_username

    @property
    def type(self):
        return self._type

    @property
    def rejector_uuid(self):
        return str(self._rejector_uuid)

    @property
    def rejector_email(self):
        return self._rejector_email

    @property
    def rejector_username(self):
        return self._rejector_username

    @property
    def properties_dict(self):
        return dict(
            type=self.type,
            rejector_uuid=self.rejector_uuid,
            rejector_email=self.rejector_email,
            rejector_username=self.rejector_username,
        )


class CanceledFriendRequestEvent:
    def __init__(self, canceler_uuid, canceler_email, canceler_username):
        self._type = "canceled_friend_request"
        self._canceler_uuid = canceler_uuid
        self._canceler_email = canceler_email
        self._canceler_username = canceler_username

    @property
    def type(self):
        return self._type

    @property
    def canceler_uuid(self):
        return str(self._canceler_uuid)

    @property
    def canceler_email(self):
        return self._canceler_email

    @property
    def canceler_username(self):
        return self._canceler_username

    @property
    def properties_dict(self):
        return dict(
            type=self.type,
            canceler_uuid=self.canceler_uuid,
            canceler_email=self.canceler_email,
            canceler_username=self.canceler_username,
        )


class NewMessageEvent:
    def __init__(self, uuid, chat_uuid, sender_uuid, sender_username, message, date, from_current_user):
        self._type = "chat_message"
        self._uuid = uuid
        self._chat_uuid = chat_uuid
        self._sender_uuid = sender_uuid
        self._sender_username = sender_username
        self._message = message
        self._date = date
        self._from_current_user = from_current_user

    @property
    def type(self):
        return self._type

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def chat_uuid(self):
        return str(self._chat_uuid)

    @property
    def sender_uuid(self):
        return str(self._sender_uuid)

    @property
    def sender_username(self):
        return self._sender_username

    @property
    def message(self):
        return self._message

    @property
    def date(self):
        return self._date.strftime(WEBSOCKET_DATETIME_FORMAT)

    @property
    def from_current_user(self):
        return str(self._from_current_user)

    @property
    def properties_dict(self):
        return dict(
            type=self.type,
            uuid=self.uuid,
            chat_uuid=self.chat_uuid,
            sender_uuid=self.sender_uuid,
            sender_username=self.sender_username,
            message=self.message,
            date=self.date,
            from_current_user=self.from_current_user,
        )
