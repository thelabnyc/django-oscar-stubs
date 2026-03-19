from decimal import Decimal
from typing import Protocol

class TaxNotKnown(Exception): ...

class PriceLike(Protocol):
    @property
    def excl_tax(self) -> Decimal: ...
    @property
    def incl_tax(self) -> Decimal | None: ...
    @property
    def is_tax_known(self) -> bool: ...

class Price:
    currency: str
    excl_tax: Decimal
    incl_tax: Decimal | None
    is_tax_known: bool
    tax_code: str | None
    tax: Decimal
    def __init__(
        self,
        currency: str,
        excl_tax: Decimal,
        incl_tax: Decimal | None = ...,
        tax: Decimal | None = ...,
        tax_code: str | None = ...,
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __add__(self, other: Price) -> Price: ...
    def __radd__(self, other: int | Price) -> Price: ...
