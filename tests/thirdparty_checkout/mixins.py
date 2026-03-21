from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http import HttpRequest
from oscar.core.loading import get_class, get_model

OrderCreator = get_class("order.utils", "OrderCreator")
Order = get_model("order", "Order")


class OrderCreatorMixin(OrderCreator):
    def custom_mixin_method(self) -> str:
        return "mixin"

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
        raise NotImplementedError

    def update_order_status(self, order: Order, new_status: str) -> Order:
        raise NotImplementedError
