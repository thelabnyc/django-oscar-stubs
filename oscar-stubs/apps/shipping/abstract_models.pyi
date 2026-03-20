from decimal import Decimal
from typing import Any, ClassVar

from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.expressions import Combinable
from django.utils.functional import _StrPromise
from oscar.core.prices import Price
from oscar.models.fields import AutoSlugField

class AbstractBase(models.Model):
    code: AutoSlugField
    name: models.CharField[str | int | Combinable, str]
    description: models.TextField[str | Combinable, str]
    countries: ManyToManyField[Any, Any]

    is_discounted: ClassVar[bool]

    def discount(self, basket: Any) -> Decimal: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractOrderAndItemCharges(AbstractBase):
    price_per_order: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    price_per_item: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    free_shipping_threshold: models.DecimalField[str | float | Decimal | None | Combinable, Decimal | None]

    def calculate(self, basket: Any) -> Price: ...

    class Meta(AbstractBase.Meta):
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractWeightBased(AbstractBase):
    weight_attribute: ClassVar[str]

    default_weight: models.DecimalField[str | float | Decimal | Combinable, Decimal]

    def calculate(self, basket: Any) -> Price: ...
    def get_charge(self, weight: Decimal) -> Decimal: ...
    def get_band_for_weight(self, weight: Decimal) -> AbstractWeightBand | None: ...
    @property
    def num_bands(self) -> int: ...
    @property
    def top_band(self) -> AbstractWeightBand | None: ...

    class Meta(AbstractBase.Meta):
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractWeightBand(models.Model):
    method: ForeignKey[AbstractWeightBased | Combinable, AbstractWeightBased]
    method_id: int
    upper_limit: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    charge: models.DecimalField[str | float | Decimal | Combinable, Decimal]

    @property
    def weight_from(self) -> Decimal: ...
    @property
    def weight_to(self) -> Decimal: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]
