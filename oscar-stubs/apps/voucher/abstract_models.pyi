from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar

from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.expressions import Combinable

class AbstractVoucherSet(models.Model):
    name: models.CharField[str | int | Combinable, str]
    count: models.PositiveIntegerField[float | int | str | Combinable, int]
    code_length: models.IntegerField[float | int | str | Combinable, int]
    description: models.TextField[str | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]
    start_datetime: models.DateTimeField[str | datetime | Combinable, datetime]
    end_datetime: models.DateTimeField[str | datetime | Combinable, datetime]

    def clean(self) -> None: ...
    def update_count(self) -> None: ...
    def is_active(self, test_datetime: datetime | None = ...) -> bool: ...
    @property
    def num_basket_additions(self) -> int | None: ...
    @property
    def num_orders(self) -> int | None: ...
    @property
    def total_discount(self) -> Decimal | None: ...

    class Meta:
        abstract: bool
        app_label: str
        get_latest_by: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractVoucher(models.Model):
    SINGLE_USE: ClassVar[str]
    MULTI_USE: ClassVar[str]
    ONCE_PER_CUSTOMER: ClassVar[str]
    USAGE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    name: models.CharField[str | int | Combinable, str]
    code: models.CharField[str | int | Combinable, str]
    offers: ManyToManyField[Any, Any]
    usage: models.CharField[str | int | Combinable, str]
    start_datetime: models.DateTimeField[str | datetime | Combinable, datetime]
    end_datetime: models.DateTimeField[str | datetime | Combinable, datetime]
    num_basket_additions: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_orders: models.PositiveIntegerField[float | int | str | Combinable, int]
    total_discount: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    voucher_set: ForeignKey[Any | None | Combinable, Any | None]
    date_created: models.DateTimeField[str | Combinable, Any]

    def clean(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def is_active(self, test_datetime: datetime | None = ...) -> bool: ...
    def is_expired(self) -> bool: ...
    def is_available_to_user(self, user: Any = ...) -> tuple[bool, str]: ...
    def is_available_for_basket(self, basket: Any) -> tuple[bool, str]: ...
    def record_usage(self, order: Any, user: Any) -> None: ...
    def record_discount(self, discount: dict[str, Any]) -> None: ...
    @property
    def benefit(self) -> Any: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        get_latest_by: str
        verbose_name: str
        verbose_name_plural: str

class AbstractVoucherApplication(models.Model):
    voucher: ForeignKey[Any | Combinable, Any]
    user: ForeignKey[Any | None | Combinable, Any | None]
    order: ForeignKey[Any | Combinable, Any]
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str
