from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from oscar.apps.catalogue.abstract_models import AbstractProduct

class AbstractProductRecord(models.Model):
    product: models.OneToOneField[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    num_views: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_basket_additions: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_purchases: models.PositiveIntegerField[float | int | str | Combinable, int]
    score: models.FloatField[float | int | str | Combinable, float]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

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
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

class AbstractUserProductView(models.Model):
    user: ForeignKey[User | Combinable, User]
    user_id: int
    product: ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractUserSearch(models.Model):
    user: ForeignKey[User | Combinable, User]
    user_id: int
    query: models.CharField[str | int | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str
