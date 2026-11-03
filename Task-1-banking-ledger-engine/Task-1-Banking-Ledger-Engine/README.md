# Banking & Ledger Engine

A Python-based object-oriented banking system demonstrating
account management, transaction tracking, and multi-currency
transfers.

## Features

- Abstract Account base class
- Savings, Checking, and High-Yield accounts
- Encapsulation and inheritance
- Polymorphic interest and fee processing
- Deposit and withdrawal validation
- Transaction ledger with timestamps
- Multi-currency transfers using explicit exchange rates
- Automated unit tests

## Requirements

- Python 3.10 or newer
- No external dependencies

## Run the application

```bash
python main.py
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## OOP Concepts

- Abstraction: Account defines the required operations.
- Encapsulation: Account data is stored in private attributes.
- Inheritance: Three account types extend Account.
- Polymorphism: Each account implements its own interest
  and fee rules.

## Limitations

- Exchange rates must be provided manually.
- This is an educational project, not a production banking system.
- No database or persistent storage is configured yet.
-