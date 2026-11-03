import unittest
from decimal import Decimal

from banking.accounts import (
    Account,
    SavingsAccount,
    CheckingAccount,
    HighYieldAccount,
)
from banking.ledger import Ledger


class BankingTests(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.savings = SavingsAccount(
            "S1", "Test User", balance="1200",
            interest_rate="0.12"
        )

    def test_deposit(self):
        self.ledger.deposit(self.savings, "100")
        self.assertEqual(self.savings.balance, Decimal("1300.00"))

    def test_withdrawal(self):
        self.ledger.withdraw(self.savings, "200")
        self.assertEqual(self.savings.balance, Decimal("1000.00"))

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.savings.withdraw("5000")

    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.savings.deposit("-10")

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Account("A1", "User", "INR")

    def test_savings_interest(self):
        interest = self.savings.accrue_interest()
        self.assertEqual(interest, Decimal("12.00"))
        self.assertEqual(self.savings.balance, Decimal("1212.00"))

    def test_checking_fee(self):
        account = CheckingAccount(
            "C1", "User", balance="100",
            monthly_fee="25"
        )
        fee = account.deduct_fees()
        self.assertEqual(fee, Decimal("25.00"))
        self.assertEqual(account.balance, Decimal("75.00"))

    def test_high_yield_interest(self):
        account = HighYieldAccount(
            "H1", "User", balance="1000",
            interest_rate="0.12", monthly_fee="10"
        )
        interest = account.accrue_interest()
        self.assertEqual(interest, Decimal("10.00"))

    def test_polymorphic_processing(self):
        accounts = [
            SavingsAccount("S2", "User", balance="1200",
                           interest_rate="0.12"),
            CheckingAccount("C2", "User", balance="1000"),
            HighYieldAccount("H2", "User", balance="1200"),
        ]

        results = [
            self.ledger.process_period(account)
            for account in accounts
        ]

        self.assertEqual(len(results), 3)
        self.assertEqual(
            results[0]["interest"], Decimal("12.00")
        )
        self.assertEqual(
            results[1]["fee"], Decimal("25.00")
        )

    def test_currency_transfer(self):
        source = SavingsAccount(
            "S3", "User", "INR", balance="5000"
        )
        target = SavingsAccount(
            "S4", "User", "USD", balance="100"
        )

        result = self.ledger.transfer(
            source, target, "1000", "0.01"
        )

        self.assertEqual(result["received"], Decimal("10.00"))
        self.assertEqual(source.balance, Decimal("4000.00"))
        self.assertEqual(target.balance, Decimal("110.00"))

    def test_failed_transfer_changes_nothing(self):
        source = SavingsAccount(
            "S5", "User", balance="100"
        )
        target = SavingsAccount(
            "S6", "User", balance="50"
        )

        with self.assertRaises(ValueError):
            self.ledger.transfer(source, target, "200")

        self.assertEqual(source.balance, Decimal("100.00"))
        self.assertEqual(target.balance, Decimal("50.00"))
        self.assertEqual(len(self.ledger.transactions), 0)


if __name__ == "__main__":
    unittest.main()