from oscar.apps.order import utils as oscar_utils

from tests.thirdparty_checkout.mixins import OrderCreatorMixin


class OrderCreator(OrderCreatorMixin, oscar_utils.OrderCreator):
    def forked_method(self) -> str:
        return "forked"
