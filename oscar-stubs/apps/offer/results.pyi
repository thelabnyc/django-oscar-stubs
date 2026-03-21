from collections.abc import Iterator, ValuesView
from decimal import Decimal
from typing import Any, ClassVar, NotRequired, TypedDict

class OfferApplication(TypedDict):
    offer: Any
    result: ApplicationResult
    name: str
    description: str | None
    voucher: Any
    freq: int
    discount: Decimal
    message: NotRequired[str]

class OfferApplications:
    applications: dict[int, OfferApplication]

    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OfferApplication]: ...
    def __len__(self) -> int: ...
    def add(self, offer: Any, result: Any) -> None: ...
    @property
    def offer_discounts(self) -> list[OfferApplication]: ...
    @property
    def voucher_discounts(self) -> list[OfferApplication]: ...
    @property
    def shipping_discounts(self) -> list[OfferApplication]: ...
    @property
    def grouped_voucher_discounts(self) -> ValuesView[dict[str, Any]]: ...
    @property
    def post_order_actions(self) -> list[OfferApplication]: ...
    @property
    def offers(self) -> dict[int, Any]: ...

class ApplicationResult:
    is_final: ClassVar[bool]
    @property
    def is_successful(self) -> bool: ...
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
    def is_successful(self) -> bool: ...

ZERO_DISCOUNT: BasketDiscount

class ShippingDiscount(ApplicationResult):
    is_successful: ClassVar[bool]
    is_final: ClassVar[bool]
    affects: ClassVar[int]

SHIPPING_DISCOUNT: ShippingDiscount

class PostOrderAction(ApplicationResult):
    is_final: ClassVar[bool]
    is_successful: ClassVar[bool]
    affects: ClassVar[int]
    description: str

    def __init__(self, description: str) -> None: ...
