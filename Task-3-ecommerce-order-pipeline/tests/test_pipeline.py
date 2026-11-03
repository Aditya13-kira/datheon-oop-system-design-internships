import unittest
from decimal import Decimal

from ecommerce.models import (
    Product, OrderItem, Order, OrderStatus
)
from ecommerce.payment import SimulatedPaymentProcessor
from ecommerce.pipeline import OrderPipeline


class TestOrderPipeline(unittest.TestCase):

    def setUp(self):
        self.product = Product("Keyboard", Decimal("500"), 10)
        self.order = Order(
            "Test Customer",
            [OrderItem(self.product, 2)]
        )

    def test_total_calculation(self):
        self.assertEqual(self.order.total, Decimal("1000.00"))

    def test_successful_payment(self):
        pipeline = OrderPipeline(
            SimulatedPaymentProcessor(True)
        )
        pipeline.process(self.order)

        self.assertEqual(
            self.order.status, OrderStatus.PROCESSING
        )
        self.assertEqual(self.product.stock, 8)

    def test_failed_payment_does_not_reduce_stock(self):
        pipeline = OrderPipeline(
            SimulatedPaymentProcessor(False)
        )
        pipeline.process(self.order)

        self.assertEqual(
            self.order.status, OrderStatus.PAYMENT_FAILED
        )
        self.assertEqual(self.product.stock, 10)

    def test_shipped_status(self):
        pipeline = OrderPipeline(
            SimulatedPaymentProcessor(True)
        )
        pipeline.process(self.order)
        pipeline.update_status(self.order, OrderStatus.SHIPPED)

        self.assertEqual(self.order.status, OrderStatus.SHIPPED)

    def test_invalid_status_transition(self):
        pipeline = OrderPipeline(
            SimulatedPaymentProcessor(True)
        )

        with self.assertRaises(ValueError):
            pipeline.update_status(
                self.order, OrderStatus.DELIVERED
            )


if __name__ == "__main__":
    unittest.main()