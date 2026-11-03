from notifications.base import Notification
from notifications.channels import (
    EmailChannel,
    SMSChannel,
    PushChannel
)
from notifications.dispatcher import NotificationDispatcher

def main():
    dispatcher = NotificationDispatcher()

    dispatcher.register_channel("email", EmailChannel())
    dispatcher.register_channel("sms", SMSChannel())
    dispatcher.register_channel("push", PushChannel())

    email = Notification(
        recipient="student@example.com",
        subject="Welcome!",
        message="Welcome to our application."
    )

    sms = Notification(
        recipient="+910000000000",
        subject="Login Alert",
        message="Your login was successful."
    )

    push = Notification(
        recipient="user_101",
        subject="New Update",
        message="You have a new notification."
    )

    dispatcher.dispatch("email", email)
    dispatcher.dispatch("sms", sms)
    dispatcher.dispatch("push", push)

if __name__ == "__main__":
    main()