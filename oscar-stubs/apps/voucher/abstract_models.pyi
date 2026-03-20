from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.expressions import Combinable
from django.utils.functional import _StrPromise
from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.offer.abstract_models import AbstractBenefit, AbstractConditionalOffer
from oscar.apps.offer.results import OfferApplication
from oscar.apps.order.abstract_models import AbstractOrder

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
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        get_latest_by: str
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractVoucher(models.Model):
    SINGLE_USE: ClassVar[str]
    MULTI_USE: ClassVar[str]
    ONCE_PER_CUSTOMER: ClassVar[str]
    USAGE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    name: models.CharField[str | int | Combinable, str]
    code: models.CharField[str | int | Combinable, str]
    offers: ManyToManyField[AbstractConditionalOffer, AbstractConditionalOffer]
    usage: models.CharField[str | int | Combinable, str]
    start_datetime: models.DateTimeField[str | datetime | Combinable, datetime]
    end_datetime: models.DateTimeField[str | datetime | Combinable, datetime]
    num_basket_additions: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_orders: models.PositiveIntegerField[float | int | str | Combinable, int]
    total_discount: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    voucher_set: ForeignKey[AbstractVoucherSet | None | Combinable, AbstractVoucherSet | None]
    voucher_set_id: int | None
    date_created: models.DateTimeField[str | Combinable, Any]

    def clean(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def is_active(self, test_datetime: datetime | None = ...) -> bool: ...
    def is_expired(self) -> bool: ...
    def is_available_to_user(self, user: AbstractBaseUser | AnonymousUser | None = ...) -> tuple[bool, str]: ...
    def is_available_for_basket(self, basket: AbstractBasket) -> tuple[bool, str]: ...
    def record_usage(
        self, order: AbstractOrder, user: User | AnonymousUser | None, *args: Any, **kwargs: Any
    ) -> None: ...
    def record_discount(self, discount: OfferApplication | dict[str, Any], *args: Any, **kwargs: Any) -> None: ...
    @property
    def benefit(self) -> AbstractBenefit | None: ...
    def get_usage_display(self) -> str: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        get_latest_by: str
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]

class AbstractVoucherApplication(models.Model):
    voucher: ForeignKey[AbstractVoucher | Combinable, AbstractVoucher]
    voucher_id: int
    user: ForeignKey[User | None | Combinable, User | None]
    user_id: int | None
    order: ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str | _StrPromise]
        verbose_name_plural: ClassVar[str | _StrPromise]
