from decimal import Decimal
from typing import Any, ClassVar

from oscar.core.prices import Price

class Base:
    code: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    is_discounted: ClassVar[bool]

    def calculate(self, basket: Any) -> Price: ...
    def discount(self, basket: Any) -> Decimal: ...

class Free(Base):
    code: ClassVar[str]
    name: ClassVar[str]

    def calculate(self, basket: Any) -> Price: ...

class NoShippingRequired(Free):
    code: ClassVar[str]
    name: ClassVar[str]

class FixedPrice(Base):
    code: ClassVar[str]
    name: ClassVar[str]
    charge_excl_tax: Decimal | None
    charge_incl_tax: Decimal | None

    def __init__(self, charge_excl_tax: Decimal | None = ..., charge_incl_tax: Decimal | None = ...) -> None: ...
    def calculate(self, basket: Any) -> Price: ...

class OfferDiscount(Base):
    is_discounted: ClassVar[bool]
    method: Base
    offer: Any

    def __init__(self, method: Base, offer: Any) -> None: ...
    @property
    def code(self) -> str: ...  # type: ignore[override]
    @property
    def name(self) -> str: ...  # type: ignore[override]
    @property
    def discount_name(self) -> str: ...
    @property
    def description(self) -> str: ...  # type: ignore[override]
    def calculate_excl_discount(self, basket: Any) -> Price: ...

class TaxExclusiveOfferDiscount(OfferDiscount):
    def calculate(self, basket: Any) -> Price: ...
    def discount(self, basket: Any) -> Decimal: ...

class TaxInclusiveOfferDiscount(OfferDiscount):
    def calculate(self, basket: Any) -> Price: ...
    def calculate_excl_tax(self, base_charge: Price, incl_tax: Decimal) -> Decimal: ...
    def discount(self, basket: Any) -> Decimal: ...
