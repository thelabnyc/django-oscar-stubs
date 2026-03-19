from typing import Any

from django.http import HttpRequest
from oscar.core.prices import Price, PriceLike

class OrderTotalCalculator:
    request: HttpRequest | None

    def __init__(self, request: HttpRequest | None = ...) -> None: ...
    def calculate(
        self, basket: Any, shipping_charge: PriceLike, surcharges: Any | None = ..., **kwargs: Any
    ) -> Price: ...
