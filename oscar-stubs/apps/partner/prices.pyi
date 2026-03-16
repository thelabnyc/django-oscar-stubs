from decimal import Decimal
from typing import ClassVar

class Base:
    exists: ClassVar[bool]
    is_tax_known: ClassVar[bool]
    excl_tax: Decimal | None
    incl_tax: Decimal | None
    tax: Decimal | None
    tax_code: str | None
    retail: Decimal | None
    currency: str | None

    @property
    def effective_price(self) -> Decimal | None: ...

class Unavailable(Base): ...

class FixedPrice(Base):
    exists: ClassVar[bool]
    currency: str
    excl_tax: Decimal
    tax: Decimal | None
    tax_code: str | None

    def __init__(
        self, currency: str, excl_tax: Decimal, tax: Decimal | None = ..., tax_code: str | None = ...
    ) -> None: ...
    @property
    def incl_tax(self) -> Decimal: ...
    @property
    def is_tax_known(self) -> bool: ...  # type: ignore[override]

class TaxInclusiveFixedPrice(FixedPrice):
    exists: ClassVar[bool]
    is_tax_known: ClassVar[bool]  # type: ignore[assignment]

    @property
    def incl_tax(self) -> Decimal: ...
    @property
    def effective_price(self) -> Decimal: ...
