from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import uuid4


def money(value):
    amount = Decimal(str(value))
    if not amount.is_finite():
        raise ValueError("Amount must be finite.")
    return amount.quantize(Decimal("0.01"))


@dataclass
class Product:
    name: str
    price: Decimal
    stock: int

    def __post_init__(self):
        self.price = money(self.price)

        if not self.name.strip():
            raise ValueError("Product name cannot be empty.")
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")


@dataclass
class OrderItem:
    product: Product
    quantity: int

    def __post_init__(self):
        if isinstance(self.quantity, bool) or self.quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not isinstance(self.quantity, int):
            raise ValueError("Quantity must be an integer.")
        if self.quantity > self.product.stock:
            raise ValueError("Insufficient stock.")

    @property
    def subtotal(self):
        return money(self.product.price * self.quantity)


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    PAYMENT_FAILED = "payment_failed"


@dataclass
class Order:
    customer_name: str
    items: list
    order_id: str = field(default_factory=lambda: str(uuid4())[:8])
    status: OrderStatus = OrderStatus.PENDING

    def __post_init__(self):
        if not self.customer_name.strip():
            raise ValueError("Customer name cannot be empty.")
        if not self.items:
            raise ValueError("Order must contain at least one item.")

    @property
    def total(self):
        return money(sum(
            (item.subtotal for item in self.items),
            Decimal("0.00")
        ))