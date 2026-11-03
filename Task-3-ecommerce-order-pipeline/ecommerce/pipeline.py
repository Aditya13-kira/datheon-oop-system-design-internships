from ecommerce.models import OrderStatus


class OrderPipeline:

    def __init__(self, payment_processor):
        self.payment_processor = payment_processor
        self.history = []

    def process(self, order):
        if order.status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be processed.")

        # Check stock before payment.
        for item in order.items:
            if item.quantity > item.product.stock:
                raise ValueError(
                    f"Insufficient stock for {item.product.name}."
                )

        payment_success = self.payment_processor.pay(order.total)

        if not payment_success:
            order.status = OrderStatus.PAYMENT_FAILED
            self.history.append(
                (order.order_id, order.status.value)
            )
            return order

        # Reduce stock only after successful payment.
        for item in order.items:
            item.product.stock -= item.quantity

        order.status = OrderStatus.PAID
        self.history.append((order.order_id, order.status.value))

        order.status = OrderStatus.PROCESSING
        self.history.append((order.order_id, order.status.value))

        return order

    def update_status(self, order, new_status):
        allowed = {
            OrderStatus.PROCESSING: {
                OrderStatus.SHIPPED,
                OrderStatus.CANCELLED
            },
            OrderStatus.SHIPPED: {
                OrderStatus.DELIVERED
            }
        }

        if new_status not in allowed.get(order.status, set()):
            raise ValueError(
                f"Cannot change status from "
                f"{order.status.value} to {new_status.value}."
            )

        order.status = new_status
        self.history.append((order.order_id, order.status.value))