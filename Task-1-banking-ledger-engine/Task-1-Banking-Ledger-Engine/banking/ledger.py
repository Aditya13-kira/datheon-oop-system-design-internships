from decimal import Decimal
from datetime import datetime, timezone

from banking.accounts import money, validate_positive


class Ledger:
    def __init__(self):
        self.__transactions = []

    @property
    def transactions(self):
        # Return a copy so external code cannot change the ledger list.
        return [dict(item) for item in self.__transactions]

    def _record(self, transaction_type, account_id,
                amount, currency, details=""):
        self.__transactions.append({
            "transaction_id": len(self.__transactions) + 1,
            "type": transaction_type,
            "account_id": account_id,
            "amount": str(money(amount)),
            "currency": currency,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def deposit(self, account, amount):
        amount = validate_positive(amount)
        account.deposit(amount)
        self._record("DEPOSIT", account.account_id, amount,
                     account.currency)
        return account.balance

    def withdraw(self, account, amount):
        amount = validate_positive(amount)
        account.withdraw(amount)
        self._record("WITHDRAWAL", account.account_id, amount,
                     account.currency)
        return account.balance

    def process_period(self, account):
        result = account.process_period()

        if result["interest"] > 0:
            self._record(
                "INTEREST", account.account_id,
                result["interest"], account.currency
            )

        if result["fee"] > 0:
            self._record(
                "FEE", account.account_id,
                result["fee"], account.currency
            )

        return result

    def transfer(self, source, target, amount, exchange_rate=1):
        amount = validate_positive(amount)
        rate = Decimal(str(exchange_rate))

        if rate <= 0:
            raise ValueError("Exchange rate must be positive.")

        if source.account_id == target.account_id:
            raise ValueError("Cannot transfer to the same account.")

        if source.currency == target.currency and rate != 1:
            raise ValueError(
                "Use exchange rate 1 for the same currency."
            )

        converted = money(amount * rate)

        if converted <= 0:
            raise ValueError("Converted amount must be positive.")

        # Validate source funds before changing either account.
        if amount > source.balance:
            raise ValueError("Insufficient funds.")

        # Execute the transfer and record it.
        source.withdraw(amount)
        target._credit(converted)

        self._record(
            "TRANSFER_OUT", source.account_id, amount,
            source.currency,
            f"To {target.account_id}"
        )
        self._record(
            "TRANSFER_IN", target.account_id, converted,
            target.currency,
            f"From {source.account_id}; rate={rate}"
        )

        return {
            "sent": amount,
            "sent_currency": source.currency,
            "received": converted,
            "received_currency": target.currency,
            "exchange_rate": rate,
        }