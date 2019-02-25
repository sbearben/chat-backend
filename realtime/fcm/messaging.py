# realtime/fcm/messaging.py
from firebase_admin import messaging
from firebase_admin.messaging import ApiCallError

from . import default_app
from .models import UserRegistrationToken


def send_event_via_fcm(user, realtime_event_dict):
    token = UserRegistrationToken.objects.get_token_if_exists(user)

    print("Firebase: send_event_via_fcm - pre send")
    if token is not None and token != "":
        message = messaging.Message(
            data=realtime_event_dict,
            token=token,
        )
        try:
            response = messaging.send(message=message, dry_run=False, app=default_app)
            print("Firebase: send_event_via_fcm - post send: " + response)
        except (ApiCallError, ValueError) as e:
            print("Firebase: messaging.send(..) failed: " + str(e))
    else:
        print("No valid FCM token for user.")


'''      
message = messaging.Message(
            data=event.properties_dict,
            android=messaging.AndroidConfig(
                ttl=0,
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='A notification title',
                    body='A notification body',
                    #color='#f45342'
                ),
            ),
            token=token,
        )
'''