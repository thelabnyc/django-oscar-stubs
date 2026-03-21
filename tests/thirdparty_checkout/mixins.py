from oscar.core.loading import get_class

OrderCreator = get_class("order.utils", "OrderCreator")


class OrderCreatorMixin(OrderCreator):  # type: ignore[misc]
    def custom_mixin_method(self) -> str:
        return "mixin"
