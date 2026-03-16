from decimal import Decimal
from typing import Any

class EventHandler:
    user: Any
    kwargs: dict[str, Any]

    def __init__(self, user: Any | None = ..., **kwargs: Any) -> None: ...

    # Core API
    def handle_shipping_event(
        self, order: Any, event_type: Any, lines: list[Any], line_quantities: list[int], **kwargs: Any
    ) -> Any: ...
    def handle_payment_event(
        self,
        order: Any,
        event_type: Any,
        amount: Decimal,
        lines: list[Any] | None = ...,
        line_quantities: list[int] | None = ...,
        **kwargs: Any,
    ) -> Any: ...
    def handle_order_status_change(self, order: Any, new_status: str, note_msg: str | None = ...) -> None: ...

    # Validation methods
    def validate_shipping_event(
        self, order: Any, event_type: Any, lines: list[Any], line_quantities: list[int], **kwargs: Any
    ) -> None: ...
    def validate_payment_event(
        self,
        order: Any,
        event_type: Any,
        amount: Decimal,
        lines: list[Any] | None = ...,
        line_quantities: list[int] | None = ...,
        **kwargs: Any,
    ) -> None: ...

    # Query methods
    def have_lines_passed_shipping_event(
        self, order: Any, lines: list[Any], line_quantities: list[int], event_type: Any
    ) -> bool: ...

    # Payment
    def calculate_payment_event_subtotal(
        self, event_type: Any, lines: list[Any], line_quantities: list[int]
    ) -> Decimal: ...

    # Stock
    def are_stock_allocations_available(self, lines: list[Any], line_quantities: list[int]) -> bool: ...
    def consume_stock_allocations(
        self, order: Any, lines: list[Any] | None = ..., line_quantities: list[int] | None = ...
    ) -> None: ...
    def cancel_stock_allocations(
        self, order: Any, lines: list[Any] | None = ..., line_quantities: list[int] | None = ...
    ) -> None: ...

    # Model instance creation
    def create_shipping_event(
        self, order: Any, event_type: Any, lines: list[Any], line_quantities: list[int], **kwargs: Any
    ) -> Any: ...
    def create_payment_event(
        self,
        order: Any,
        event_type: Any,
        amount: Decimal,
        lines: list[Any] | None = ...,
        line_quantities: list[int] | None = ...,
        **kwargs: Any,
    ) -> Any: ...
    def create_communication_event(self, order: Any, event_type: Any) -> Any: ...
    def create_note(self, order: Any, message: str, note_type: str = ...) -> Any: ...
