from banking.accounts import (
    SavingsAccount,
    CheckingAccount,
    HighYieldAccount,
)
from banking.ledger import Ledger


def main():
    ledger = Ledger()

    savings = SavingsAccount(
        "ACC101", "Aditya", "INR",
        balance="10000", interest_rate="0.04"
    )
    checking = CheckingAccount(
        "ACC102", "Aditya", "INR",
        balance="5000", monthly_fee="25"
    )
    high_yield = HighYieldAccount(
        "ACC103", "Aditya", "USD",
        balance="1000", interest_rate="0.06"
    )

    accounts = [savings, checking, high_yield]

    print("=== BANKING LEDGER ENGINE ===")

    for account in accounts:
        print(account)

    print("\n=== DEPOSIT ===")
    ledger.deposit(savings, "500")
    print(savings)

    print("\n=== WITHDRAWAL ===")
    ledger.withdraw(checking, "200")
    print(checking)

    print("\n=== PERIOD PROCESSING ===")
    for account in accounts:
        result = ledger.process_period(account)
        print(result)

    print("\n=== MULTI-CURRENCY TRANSFER ===")
    result = ledger.transfer(
        savings, high_yield,
        amount="1000",
        exchange_rate="0.011"
    )
    print(result)

    print("\n=== TRANSACTION HISTORY ===")
    for transaction in ledger.transactions:
        print(transaction)


if __name__ == "__main__":
    main()