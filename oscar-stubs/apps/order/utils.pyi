from typing import Any, ClassVar

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http import HttpRequest
from oscar.apps.offer.results import OfferApplication

class OrderNumberGenerator:
    def order_number(self, basket: Any) -> str | int: ...

class OrderCreator:
    def place_order(
        self,
        basket: Any,
        total: Any,
        shipping_method: Any,
        shipping_charge: Any,
        user: AbstractBaseUser | AnonymousUser | None = ...,
        shipping_address: Any | None = ...,
        billing_address: Any | None = ...,
        order_number: str | int | None = ...,
        status: str | None = ...,
        request: HttpRequest | None = ...,
        surcharges: list[Any] | None = ...,
        **kwargs: Any,
    ) -> Any: ...
    def create_order_model(
        self,
        user: AbstractBaseUser | AnonymousUser | None,
        basket: Any,
        shipping_address: Any | None,
        shipping_method: Any,
        shipping_charge: Any,
        billing_address: Any | None,
        total: Any,
        order_number: str | int,
        status: str | None,
        request: HttpRequest | None = ...,
        surcharges: list[Any] | None = ...,
        **extra_order_fields: Any,
    ) -> Any: ...
    def create_line_models(
        self, order: Any, basket_line: Any, extra_line_fields: dict[str, Any] | None = ...
    ) -> Any: ...
    def update_stock_records(self, line: Any) -> None: ...
    def create_line_discount_models(self, order: Any, order_line: Any, basket_line: Any) -> None: ...
    def create_additional_line_models(self, order: Any, order_line: Any, basket_line: Any) -> None: ...
    def create_line_price_models(self, order: Any, order_line: Any, basket_line: Any) -> None: ...
    def create_line_attributes(self, order: Any, order_line: Any, basket_line: Any) -> None: ...
    def create_discount_model(self, order: Any, discount: OfferApplication) -> None: ...
    def record_discount(self, discount: OfferApplication) -> None: ...
    def record_voucher_usage(self, order: Any, voucher: Any, user: AbstractBaseUser | AnonymousUser | None) -> None: ...

class OrderDispatcher:
    ORDER_PLACED_EVENT_CODE: ClassVar[str]
    dispatcher: Any

    def __init__(self, logger: Any | None = ..., mail_connection: Any | None = ...) -> None: ...
    def dispatch_order_messages(
        self, order: Any, messages: Any, event_code: str, attachments: Any | None = ..., **kwargs: Any
    ) -> None: ...
    def create_communication_event(self, order: Any, event_type: Any, dispatched_messages: Any) -> None: ...
    def send_order_placed_email_for_user(
        self, order: Any, extra_context: dict[str, Any], attachments: Any | None = ...
    ) -> None: ...
