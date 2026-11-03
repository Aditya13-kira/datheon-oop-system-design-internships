from notifications.base import Notification, NotificationChannel

class NotificationDispatcher:

    def __init__(self):
        self.channels = {}

    def register_channel(
        self,
        name: str,
        channel: NotificationChannel
    ):
        self.channels[name.lower()] = channel

    def dispatch(
        self,
        channel_name: str,
        notification: Notification
    ) -> bool:

        channel = self.channels.get(channel_name.lower())

        if channel is None:
            print(f"Error: Unknown channel '{channel_name}'")
            return False

        try:
            result = channel.send(notification)

            if result:
                print("Notification dispatched successfully.")

            return result

        except Exception as error:
            print(f"Notification failed: {error}")
            return False