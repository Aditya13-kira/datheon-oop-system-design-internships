from notifications.base import Notification, NotificationChannel

class EmailChannel(NotificationChannel):

    def send(self, notification: Notification) -> bool:
        print(f"\n[EMAIL] To: {notification.recipient}")
        print(f"Subject: {notification.subject}")
        print(f"Message: {notification.message}")
        return True

class SMSChannel(NotificationChannel):

    def send(self, notification: Notification) -> bool:
        print(f"\n[SMS] To: {notification.recipient}")
        print(f"Message: {notification.message}")
        return True

class PushChannel(NotificationChannel):

    def send(self, notification: Notification) -> bool:
        print(f"\n[PUSH] To: {notification.recipient}")
        print(f"Title: {notification.subject}")
        print(f"Message: {notification.message}")
        return True