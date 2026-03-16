from decimal import Decimal
from typing import Any, ClassVar
import datetime

from django.db import models
from django.db.models.expressions import Combinable

class AbstractPartner(models.Model):
    code: models.CharField[str | Combinable, str]
    name: models.CharField[str | Combinable, str]
    users: models.ManyToManyField[Any, Any]

    @property
    def display_name(self) -> str: ...
    @property
    def primary_address(self) -> Any | None: ...
    def get_address_for_stockrecord(self, stockrecord: Any) -> Any | None: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: tuple[str, ...]
        permissions: tuple[tuple[str, str], ...]
        verbose_name: str
        verbose_name_plural: str

class AbstractStockRecord(models.Model):
    product: models.ForeignKey[Any | Combinable, Any]
    partner: models.ForeignKey[Any | Combinable, Any]
    partner_sku: models.CharField[str | Combinable, str]
    price_currency: models.CharField[str | Combinable, str]
    price: models.DecimalField[Decimal | str | Combinable | None, Decimal | None]
    num_in_stock: models.PositiveIntegerField[int | Combinable | None, int | None]
    num_allocated: models.IntegerField[int | Combinable | None, int | None]
    low_stock_threshold: models.PositiveIntegerField[int | Combinable | None, int | None]
    date_created: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]
    date_updated: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]

    class Meta:
        abstract: bool
        app_label: str
        unique_together: tuple[str, ...]
        verbose_name: str
        verbose_name_plural: str

    @property
    def net_stock_level(self) -> int: ...
    @property
    def can_track_allocations(self) -> bool: ...
    def allocate(self, quantity: int) -> None: ...
    def is_allocation_consumption_possible(self, quantity: int) -> bool: ...
    def consume_allocation(self, quantity: int) -> None: ...
    def cancel_allocation(self, quantity: int) -> None: ...
    def pre_save_signal(self) -> None: ...
    def post_save_signal(self) -> None: ...
    @property
    def is_below_threshold(self) -> bool: ...

class AbstractStockAlert(models.Model):
    stockrecord: models.ForeignKey[Any | Combinable, Any]
    threshold: models.PositiveIntegerField[int | Combinable, int]

    OPEN: ClassVar[str]
    CLOSED: ClassVar[str]
    status_choices: ClassVar[tuple[tuple[str, str], ...]]

    status: models.CharField[str | Combinable, str]
    date_created: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]
    date_closed: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]

    class Meta:
        abstract: bool
        app_label: str
        ordering: tuple[str, ...]
        verbose_name: str
        verbose_name_plural: str

    def close(self) -> None: ...
