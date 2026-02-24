import firebase_admin
from firebase_admin import credentials, messaging

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "app/security/service-account-file.json"
    )
    firebase_admin.initialize_app(cred)


class PushNotificationService:

    @staticmethod
    def send_push(token: str, title: str, message: str):

        try:
            msg = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                android=messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        sound="default"
                    ),
                ),
                apns=messaging.APNSConfig(
                    headers={"apns-priority": "10"},
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound="default",
                            badge=1
                        )
                    ),
                ),
                token=token,
            )

            return messaging.send(msg)

        except Exception as e:
            print("Push Error:", str(e))
            return None