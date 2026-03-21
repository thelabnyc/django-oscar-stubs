from oscar.apps.order.apps import OrderConfig as OscarOrderConfig


class OrderConfig(OscarOrderConfig):
    name = "tests.forked_order"
