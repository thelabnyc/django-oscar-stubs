from decimal import Decimal
from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from django.utils.functional import _StrPromise
from oscar.apps.catalogue.abstract_models import AbstractProduct

class AbstractProductRecord(models.Model):
    product: models.OneToOneField[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    num_views: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_basket_additions: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_purchases: models.PositiveIntegerField[float | int | str | Combinable, int]
    score: models.FloatField[float | int | str | Combinable, float]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractUserRecord(models.Model):
    user: models.OneToOneField[User | Combinable, User]
    user_id: int
    num_product_views: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_basket_additions: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_orders: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_order_lines: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_order_items: models.PositiveIntegerField[float | int | str | Combinable, int]
    total_spent: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    date_last_order: models.DateTimeField[str | None | Combinable, Any | None]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractUserProductView(models.Model):
    user: ForeignKey[User | Combinable, User]
    user_id: int
    product: ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractUserSearch(models.Model):
    user: ForeignKey[User | Combinable, User]
    user_id: int
    query: models.CharField[str | int | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]
