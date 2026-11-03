from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def money(value):
    """Convert a value into a two-decimal monetary amount."""
    amount = Decimal(str(value))
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def validate_positive(amount):
    amount = money(amount)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return amount


class Account(ABC):
    def __init__(self, account_id, owner, currency, balance=0):
        if not account_id.strip():
            raise ValueError("Account ID cannot be empty.")
        if not owner.strip():
            raise ValueError("Owner name cannot be empty.")
        if len(currency) != 3 or not currency.isalpha():
            raise ValueError("Currency must be a 3-letter code.")

        balance = money(balance)
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.__account_id = account_id
        self.__owner = owner
        self.__currency = currency.upper()
        self.__balance = balance

    @property
    def account_id(self):
        return self.__account_id

    @property
    def owner(self):
        return self.__owner

    @property
    def currency(self):
        return self.__currency

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        amount = validate_positive(amount)
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        amount = validate_positive(amount)

        if amount > self.__balance:
            raise ValueError("Insufficient funds.")

        self.__balance -= amount
        return self.__balance

    def _credit(self, amount):
        """Internal helper for validated account credits."""
        amount = validate_positive(amount)
        self.__balance += amount

    @abstractmethod
    def accrue_interest(self):
        """Apply the account's interest rules."""
        pass

    @abstractmethod
    def deduct_fees(self):
        """Apply the account's fee rules."""
        pass

    def process_period(self):
        """Polymorphic account processing."""
        interest = self.accrue_interest()
        fee = self.deduct_fees()

        return {
            "account_id": self.account_id,
            "interest": interest,
            "fee": fee,
            "balance": self.balance,
        }

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.account_id}, "
            f"balance={self.balance} {self.currency})"
        )


class SavingsAccount(Account):
    def __init__(
        self, account_id, owner, currency="INR",
        balance=0, interest_rate="0.04"
    ):
        super().__init__(account_id, owner, currency, balance)
        self.interest_rate = Decimal(str(interest_rate))
        if not Decimal("0") <= self.interest_rate <= Decimal("1"):
            raise ValueError("Interest rate must be between 0 and 1.")

    def accrue_interest(self):
        interest = money(self.balance * self.interest_rate / 12)
        if interest:
            self._credit(interest)
        return interest

    def deduct_fees(self):
        return money(0)


class CheckingAccount(Account):
    def __init__(
        self, account_id, owner, currency="INR",
        balance=0, monthly_fee="25.00"
    ):
        super().__init__(account_id, owner, currency, balance)
        self.monthly_fee = money(monthly_fee)
        if self.monthly_fee < 0:
            raise ValueError("Monthly fee cannot be negative.")

    def accrue_interest(self):
        return money(0)

    def deduct_fees(self):
        fee = min(self.balance, self.monthly_fee)
        fee = money(fee)
        if fee:
            self.withdraw(fee)
        return fee


class HighYieldAccount(Account):
    def __init__(
        self, account_id, owner, currency="INR",
        balance=0, interest_rate="0.06",
        monthly_fee="10.00"
    ):
        super().__init__(account_id, owner, currency, balance)
        self.interest_rate = Decimal(str(interest_rate))
        self.monthly_fee = money(monthly_fee)

        if not Decimal("0") <= self.interest_rate <= Decimal("1"):
            raise ValueError("Interest rate must be between 0 and 1.")
        if self.monthly_fee < 0:
            raise ValueError("Monthly fee cannot be negative.")

    def accrue_interest(self):
        interest = money(self.balance * self.interest_rate / 12)
        if interest:
            self._credit(interest)
        return interest

    def deduct_fees(self):
        fee = min(self.balance, self.monthly_fee)
        fee = money(fee)
        if fee:
            self.withdraw(fee)
        return fee