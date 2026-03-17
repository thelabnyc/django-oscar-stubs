from decimal import Decimal
from typing import Any

from oscar.apps.offer.abstract_models import (
    AbstractBenefit as AbstractBenefit,
)
from oscar.apps.offer.abstract_models import (
    AbstractCondition as AbstractCondition,
)
from oscar.apps.offer.abstract_models import (
    AbstractConditionalOffer as AbstractConditionalOffer,
)
from oscar.apps.offer.abstract_models import (
    AbstractRange as AbstractRange,
)
from oscar.apps.offer.abstract_models import (
    AbstractRangeProduct as AbstractRangeProduct,
)
from oscar.apps.offer.abstract_models import (
    AbstractRangeProductFileUpload as AbstractRangeProductFileUpload,
)
from oscar.apps.offer.results import (
    SHIPPING_DISCOUNT as SHIPPING_DISCOUNT,
)
from oscar.apps.offer.results import (
    ZERO_DISCOUNT as ZERO_DISCOUNT,
)
from oscar.apps.offer.results import (
    BasketDiscount as BasketDiscount,
)
from oscar.apps.offer.results import (
    PostOrderAction as PostOrderAction,
)
from oscar.apps.offer.results import (
    ShippingDiscount as ShippingDiscount,
)

class ConditionalOffer(AbstractConditionalOffer):
    id: int

class Benefit(AbstractBenefit):
    id: int

class Condition(AbstractCondition):
    id: int

class Range(AbstractRange):
    id: int

class RangeProduct(AbstractRangeProduct):
    id: int

class RangeProductFileUpload(AbstractRangeProductFileUpload):
    id: int

# Benefit proxy classes (from oscar.apps.offer.benefits)

class PercentageDiscountBenefit(Benefit):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        discount_percent: Decimal | None = ...,
        max_total_discount: Decimal | None = ...,
        **kwargs: Any,
    ) -> BasketDiscount: ...

class AbsoluteDiscountBenefit(Benefit):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        discount_amount: Decimal | None = ...,
        max_total_discount: Decimal | None = ...,
        **kwargs: Any,
    ) -> BasketDiscount: ...

class FixedUnitDiscountBenefit(AbsoluteDiscountBenefit):
    def get_lines_to_discount(
        self, offer: Any, line_tuples: list[tuple[Decimal, Any]]
    ) -> list[tuple[Any, Decimal, int]]: ...
    def apply(
        self,
        basket: Any,
        condition: Any,
        offer: Any,
        discount_amount: Decimal | None = ...,
        max_total_discount: Decimal | None = ...,
        **kwargs: Any,
    ) -> BasketDiscount: ...

class FixedPriceBenefit(Benefit):
    @property
    def name(self) -> str: ...
    def apply(self, basket: Any, condition: Any, offer: Any, **kwargs: Any) -> BasketDiscount: ...

class MultibuyDiscountBenefit(Benefit):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def apply(self, basket: Any, condition: Any, offer: Any, **kwargs: Any) -> BasketDiscount: ...

class ShippingBenefit(Benefit):
    def apply(self, basket: Any, condition: Any, offer: Any, **kwargs: Any) -> ShippingDiscount: ...

class ShippingAbsoluteDiscountBenefit(ShippingBenefit):
    @property
    def name(self) -> str: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

class ShippingFixedPriceBenefit(ShippingBenefit):
    @property
    def name(self) -> str: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

class ShippingPercentageDiscountBenefit(ShippingBenefit):
    @property
    def name(self) -> str: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

# Condition proxy classes (from oscar.apps.offer.conditions)

class CountCondition(Condition):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def is_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def is_partially_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def get_upsell_message(self, offer: Any, basket: Any) -> str | None: ...
    def consume_items(self, offer: Any, basket: Any, affected_lines: list[Any]) -> None: ...

class CoverageCondition(Condition):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def is_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def is_partially_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def get_upsell_message(self, offer: Any, basket: Any) -> str | None: ...
    def consume_items(self, offer: Any, basket: Any, affected_lines: list[Any]) -> None: ...
    def get_value_of_satisfying_items(self, offer: Any, basket: Any) -> Decimal: ...

class ValueCondition(Condition):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def is_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def is_partially_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def get_upsell_message(self, offer: Any, basket: Any) -> str | None: ...
    def consume_items(self, offer: Any, basket: Any, affected_lines: list[Any]) -> None: ...
