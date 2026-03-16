from typing import Any

from django.http import HttpRequest
from oscar.core.prices import Price

class SurchargePrice:
    surcharge: Any
    price: Price | None

    def __init__(self, surcharge: Any, price: Price | None) -> None: ...

class SurchargeList(list[SurchargePrice]):
    @property
    def total(self) -> Price: ...

class SurchargeApplicator:
    request: HttpRequest | None
    context: dict[str, Any] | None

    def __init__(
        self,
        request: HttpRequest | None = ...,
        context: dict[str, Any] | None = ...,
    ) -> None: ...
    def get_surcharges(self, basket: Any, **kwargs: Any) -> tuple[Any, ...]: ...
    def get_applicable_surcharges(self, basket: Any, **kwargs: Any) -> SurchargeList | None: ...
    def is_applicable(self, surcharge: Any, basket: Any, **kwargs: Any) -> bool: ...
