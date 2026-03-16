from collections.abc import Iterator
from decimal import Decimal
from typing import Any, ClassVar

class OfferApplications:
    applications: dict[int, dict[str, Any]]

    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[dict[str, Any]]: ...
    def __len__(self) -> int: ...
    def add(self, offer: Any, result: ApplicationResult) -> None: ...
    @property
    def offer_discounts(self) -> list[dict[str, Any]]: ...
    @property
    def voucher_discounts(self) -> list[dict[str, Any]]: ...
    @property
    def shipping_discounts(self) -> list[dict[str, Any]]: ...
    @property
    def grouped_voucher_discounts(self) -> Any: ...
    @property
    def post_order_actions(self) -> list[dict[str, Any]]: ...
    @property
    def offers(self) -> dict[int, Any]: ...

class ApplicationResult:
    is_final: ClassVar[bool]
    is_successful: ClassVar[bool]
    discount: Decimal
    description: str | None

    BASKET: ClassVar[int]
    SHIPPING: ClassVar[int]
    POST_ORDER: ClassVar[int]
    affects: ClassVar[int | None]

    @property
    def affects_basket(self) -> bool: ...
    @property
    def affects_shipping(self) -> bool: ...
    @property
    def affects_post_order(self) -> bool: ...

class BasketDiscount(ApplicationResult):
    affects: ClassVar[int]
    discount: Decimal

    def __init__(self, amount: Decimal) -> None: ...
    @property
    def is_successful(self) -> bool: ...  # type: ignore[override]

ZERO_DISCOUNT: BasketDiscount

class ShippingDiscount(ApplicationResult):
    is_successful: ClassVar[bool]  # type: ignore[assignment]
    is_final: ClassVar[bool]
    affects: ClassVar[int]

SHIPPING_DISCOUNT: ShippingDiscount

class PostOrderAction(ApplicationResult):
    is_final: ClassVar[bool]
    is_successful: ClassVar[bool]  # type: ignore[assignment]
    affects: ClassVar[int]
    description: str

    def __init__(self, description: str) -> None: ...
