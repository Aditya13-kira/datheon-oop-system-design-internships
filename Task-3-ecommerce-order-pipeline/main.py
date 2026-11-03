from decimal import Decimal

from ecommerce.models import (
    Product,
    OrderItem,
    Order,
    OrderStatus
)
from ecommerce.payment import SimulatedPaymentProcessor
from ecommerce.pipeline import OrderPipeline


def main():
    laptop = Product("Laptop", Decimal("55000.00"), stock=5)
    mouse = Product("Wireless Mouse", Decimal("1200.00"), stock=20)

    items = [
        OrderItem(laptop, 1),
        OrderItem(mouse, 2)
    ]

    order = Order(
        customer_name="Demo Customer",
        items=items
    )

    print("Order ID:", order.order_id)
    print("Customer:", order.customer_name)
    print("Order total:", order.total)
    print("Initial status:", order.status.value)

    processor = SimulatedPaymentProcessor(should_succeed=True)
    pipeline = OrderPipeline(processor)

    pipeline.process(order)

    print("Current status:", order.status.value)
    print("Remaining laptop stock:", laptop.stock)
    print("Remaining mouse stock:", mouse.stock)

    pipeline.update_status(order, OrderStatus.SHIPPED)
    print("Updated status:", order.status.value)

    pipeline.update_status(order, OrderStatus.DELIVERED)
    print("Final status:", order.status.value)

    print("\nOrder history:")
    for order_id, status in pipeline.history:
        print(order_id, "->", status)


if __name__ == "__main__":
    main()