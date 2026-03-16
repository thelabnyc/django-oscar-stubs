from decimal import Decimal
from typing import Any

class Scale:
    attribute: str
    default_weight: Decimal | None

    def __init__(
        self,
        attribute_code: str = ...,
        default_weight: Decimal | None = ...,
    ) -> None: ...
    def weigh_product(self, product: Any) -> Decimal: ...
    def weigh_basket(self, basket: Any) -> Decimal: ...
