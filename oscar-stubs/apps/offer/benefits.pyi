from decimal import Decimal
from typing import Any

from django.utils.functional import _StrPromise
from oscar.apps.offer.models import Benefit
from oscar.apps.offer.results import ApplicationResult, BasketDiscount

__all__: list[str] = [
    "PercentageDiscountBenefit",
    "AbsoluteDiscountBenefit",
    "FixedUnitDiscountBenefit",
    "FixedPriceBenefit",
    "ShippingBenefit",
    "MultibuyDiscountBenefit",
    "ShippingAbsoluteDiscountBenefit",
    "ShippingFixedPriceBenefit",
    "ShippingPercentageDiscountBenefit",
]

def apply_discount(
    line: Any,
    discount: Decimal,
    quantity: int,
    offer: Any | None = ...,
    incl_tax: bool | None = ...,
) -> None: ...

class PercentageDiscountBenefit(Benefit):
    @property
    def name(self) -> str | _StrPromise: ...
    @property
    def description(self) -> str | _StrPromise: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        discount_percent: Decimal | None = ...,
        max_total_discount: Decimal | None = ...,
        consume_items: Any | None = ...,
    ) -> BasketDiscount: ...

class AbsoluteDiscountBenefit(Benefit):
    @property
    def name(self) -> str | _StrPromise: ...
    @property
    def description(self) -> str | _StrPromise: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        discount_amount: Decimal | None = ...,
        max_total_discount: Decimal | None = ...,
        consume_items: Any | None = ...,
    ) -> BasketDiscount: ...

class FixedUnitDiscountBenefit(AbsoluteDiscountBenefit):
    def get_lines_to_discount(
        self, offer: Any, line_tuples: list[tuple[Decimal, Any]]
    ) -> list[tuple[Any, Decimal, int]]: ...

class FixedPriceBenefit(Benefit):
    @property
    def name(self) -> str | _StrPromise: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        max_total_discount: Decimal | None = ...,
        consume_items: Any | None = ...,
    ) -> BasketDiscount: ...

class MultibuyDiscountBenefit(Benefit):
    @property
    def name(self) -> str | _StrPromise: ...
    @property
    def description(self) -> str | _StrPromise: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        max_total_discount: Decimal | None = ...,
        consume_items: Any | None = ...,
    ) -> BasketDiscount: ...

class ShippingBenefit(Benefit):
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        max_total_discount: Decimal | None = ...,
        consume_items: Any | None = ...,
    ) -> ApplicationResult: ...

class ShippingAbsoluteDiscountBenefit(ShippingBenefit):
    @property
    def name(self) -> str | _StrPromise: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

class ShippingFixedPriceBenefit(ShippingBenefit):
    @property
    def name(self) -> str | _StrPromise: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

class ShippingPercentageDiscountBenefit(ShippingBenefit):
    @property
    def name(self) -> str | _StrPromise: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...
