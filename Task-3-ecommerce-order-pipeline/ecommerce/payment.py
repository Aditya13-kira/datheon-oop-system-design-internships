from abc import ABC, abstractmethod
from decimal import Decimal


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount: Decimal) -> bool:
        pass


class SimulatedPaymentProcessor(PaymentProcessor):

    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed

    def pay(self, amount: Decimal) -> bool:
        print(f"Processing simulated payment: {amount}")

        if self.should_succeed:
            print("Payment successful.")
            return True

        print("Payment failed.")
        return False