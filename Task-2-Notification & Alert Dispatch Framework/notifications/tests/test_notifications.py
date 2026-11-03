import unittest

from notifications.base import Notification
from notifications.channels import EmailChannel
from notifications.dispatcher import NotificationDispatcher

class TestNotificationDispatcher(unittest.TestCase):

    def setUp(self):
        self.dispatcher = NotificationDispatcher()
        self.dispatcher.register_channel("email", EmailChannel())

        self.notification = Notification(
            recipient="test@example.com",
            subject="Test",
            message="Hello"
        )

    def test_registered_channel(self):
        result = self.dispatcher.dispatch(
            "email", self.notification
        )
        self.assertTrue(result)

    def test_unknown_channel(self):
        result = self.dispatcher.dispatch(
            "unknown", self.notification
        )
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()