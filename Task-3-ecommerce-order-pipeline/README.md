# E-Commerce Order Pipeline

## Overview
An educational Python project that models e-commerce orders,
payment processing, inventory updates, and order status transitions.

## Features
- Product and order item models
- Decimal-based total calculation
- Stock validation
- Simulated payment processing
- Order status management
- Order processing history
- Unit tests using unittest

## Requirements
Python 3.10 or later. No third-party packages required.

## Run
python main.py

## Test
python -m unittest discover -s tests -v

## Limitations
Payments are simulated. This project does not connect to a real
payment gateway, database, inventory service, or shipping provider.
It is a learning prototype, not production commerce software.