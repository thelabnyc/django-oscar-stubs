from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http import HttpRequest
from oscar.apps.order import utils as oscar_utils

from tests.forked_order.models import Order
from tests.thirdparty_checkout.mixins import OrderCreatorMixin


class OrderCreator(OrderCreatorMixin, oscar_utils.OrderCreator):
    def forked_method(self) -> str:
        return "forked"

    def place_order(
        self,
        basket: Any,
        total: Any,
        shipping_method: Any,
        shipping_charge: Any,
        user: AbstractBaseUser | AnonymousUser | None = None,
        shipping_address: Any | None = None,
        billing_address: Any | None = None,
        order_number: str | int | None = None,
        status: str | None = None,
        request: HttpRequest | None = None,
        surcharges: list[Any] | None = None,
        **kwargs: Any,
    ) -> Order:
        return super().place_order(
            basket,
            total,
            shipping_method,
            shipping_charge,
            user=user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            order_number=order_number,
            status=status,
            request=request,
            surcharges=surcharges,
            **kwargs,
        )

    def update_order_status(self, order: Order, new_status: str) -> Order:
        return order
