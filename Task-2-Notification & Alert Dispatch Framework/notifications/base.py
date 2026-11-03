from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Notification:
    recipient: str
    subject: str
    message: str

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass