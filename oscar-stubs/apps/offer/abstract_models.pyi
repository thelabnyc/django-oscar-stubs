from decimal import Decimal
from io import IOBase
from typing import Any, ClassVar
import datetime

from django.db import models
from django.db.models.expressions import Combinable
from django.db.models.query import QuerySet
from oscar.apps.offer.results import ApplicationResult

class BaseOfferMixin(models.Model):
    class Meta:
        abstract: bool

    def proxy(self) -> BaseOfferMixin: ...
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str | None: ...

class AbstractConditionalOffer(models.Model):
    name: models.CharField[str | Combinable, str]
    slug: models.CharField[str | Combinable, str]
    description: models.TextField[str | Combinable, str]

    # Offer type constants
    SITE: ClassVar[str]
    VOUCHER: ClassVar[str]
    USER: ClassVar[str]
    SESSION: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    offer_type: models.CharField[str | Combinable, str]

    exclusive: models.BooleanField[bool | Combinable, bool]
    combinations: models.ManyToManyField[Any, Any]

    # Status constants
    OPEN: ClassVar[str]
    SUSPENDED: ClassVar[str]
    CONSUMED: ClassVar[str]

    status: models.CharField[str | Combinable, str]

    condition: models.ForeignKey[Any | Combinable, Any]
    benefit: models.ForeignKey[Any | Combinable, Any]

    priority: models.IntegerField[int | Combinable, int]

    start_datetime: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]
    end_datetime: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]

    max_global_applications: models.PositiveIntegerField[int | Combinable | None, int | None]
    max_user_applications: models.PositiveIntegerField[int | Combinable | None, int | None]
    max_basket_applications: models.PositiveIntegerField[int | Combinable | None, int | None]
    max_discount: models.DecimalField[Decimal | str | Combinable | None, Decimal | None]

    total_discount: models.DecimalField[Decimal | str | Combinable, Decimal]
    num_applications: models.PositiveIntegerField[int | Combinable, int]
    num_orders: models.PositiveIntegerField[int | Combinable, int]

    redirect_url: models.CharField[str | Combinable, str]
    date_created: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]

    objects: ClassVar[models.Manager[AbstractConditionalOffer]]
    active: ClassVar[models.Manager[AbstractConditionalOffer]]

    _voucher: Any

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def get_absolute_url(self) -> str: ...
    def clean(self) -> None: ...
    @property
    def is_voucher_offer_type(self) -> bool: ...
    @property
    def is_open(self) -> bool: ...
    @property
    def is_suspended(self) -> bool: ...
    def suspend(self) -> None: ...
    def unsuspend(self) -> None: ...
    def is_available(self, user: Any | None = ..., test_date: datetime.datetime | None = ...) -> bool: ...
    def is_condition_satisfied(self, basket: Any) -> bool: ...
    def is_condition_partially_satisfied(self, basket: Any) -> bool: ...
    def get_upsell_message(self, basket: Any) -> str | None: ...
    def apply_benefit(self, basket: Any) -> ApplicationResult: ...
    def apply_deferred_benefit(self, basket: Any, order: Any, application: dict[str, Any]) -> Any: ...
    def set_voucher(self, voucher: Any) -> None: ...
    def get_voucher(self) -> Any: ...
    def get_max_applications(self, user: Any | None = ...) -> int: ...
    def get_num_user_applications(self, user: Any) -> int: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...
    def record_usage(self, discount: dict[str, Any]) -> None: ...
    def availability_description(self) -> str: ...
    def availability_restrictions(self) -> list[dict[str, Any]]: ...
    @property
    def has_products(self) -> bool: ...
    def products(self) -> QuerySet[Any]: ...
    @property
    def combined_offers(self) -> QuerySet[AbstractConditionalOffer]: ...

class AbstractBenefit(BaseOfferMixin, models.Model):
    range: models.ForeignKey[Any | Combinable | None, Any | None]

    # Benefit type constants
    PERCENTAGE: ClassVar[str]
    FIXED: ClassVar[str]
    FIXED_UNIT: ClassVar[str]
    MULTIBUY: ClassVar[str]
    FIXED_PRICE: ClassVar[str]
    SHIPPING_PERCENTAGE: ClassVar[str]
    SHIPPING_ABSOLUTE: ClassVar[str]
    SHIPPING_FIXED_PRICE: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    type: models.CharField[str | Combinable, str]
    value: models.DecimalField[Decimal | str | Combinable | None, Decimal | None]
    max_affected_items: models.PositiveIntegerField[int | Combinable | None, int | None]
    proxy_class: models.CharField[str | Combinable | None, str | None]

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

    @property
    def proxy_map(self) -> dict[str, type]: ...
    def apply(self, basket: Any, condition: Any, offer: Any) -> ApplicationResult: ...
    def apply_deferred(self, basket: Any, order: Any, application: dict[str, Any]) -> Any: ...
    def clean(self) -> None: ...
    def clean_multibuy(self) -> None: ...
    def clean_percentage(self) -> None: ...
    def clean_shipping_absolute(self) -> None: ...
    def clean_shipping_percentage(self) -> None: ...
    def clean_shipping_fixed_price(self) -> None: ...
    def clean_fixed_price(self) -> None: ...
    def clean_absolute(self) -> None: ...
    def clean_fixed(self) -> None: ...
    def round(self, amount: Decimal, currency: str | None = ..., round_type: str = ...) -> Decimal: ...
    def _effective_max_affected_items(self) -> int: ...
    def can_apply_benefit(self, line: Any) -> bool: ...
    def get_applicable_lines(self, offer: Any, basket: Any, range: Any | None = ...) -> list[tuple[Decimal, Any]]: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...

class AbstractCondition(BaseOfferMixin, models.Model):
    COUNT: ClassVar[str]
    VALUE: ClassVar[str]
    COVERAGE: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    range: models.ForeignKey[Any | Combinable | None, Any | None]
    type: models.CharField[str | Combinable, str]
    value: models.DecimalField[Decimal | str | Combinable | None, Decimal | None]
    proxy_class: models.CharField[str | Combinable | None, str | None]

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

    @property
    def proxy_map(self) -> dict[str, type]: ...
    def clean(self) -> None: ...
    def clean_count(self) -> None: ...
    def clean_value(self) -> None: ...
    def clean_coverage(self) -> None: ...
    def consume_items(self, offer: Any, basket: Any, affected_lines: list[Any]) -> None: ...
    def is_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def is_partially_satisfied(self, offer: Any, basket: Any) -> bool: ...
    def get_upsell_message(self, offer: Any, basket: Any) -> str | None: ...
    def can_apply_condition(self, line: Any) -> bool: ...
    def get_applicable_lines(
        self, offer: Any, basket: Any, most_expensive_first: bool = ...
    ) -> list[tuple[Decimal, Any]]: ...

class AbstractRange(models.Model):
    name: models.CharField[str | Combinable, str]
    slug: models.CharField[str | Combinable, str]
    description: models.TextField[str | Combinable, str]
    is_public: models.BooleanField[bool | Combinable, bool]
    includes_all_products: models.BooleanField[bool | Combinable, bool]

    included_products: models.ManyToManyField[Any, Any]
    excluded_products: models.ManyToManyField[Any, Any]
    classes: models.ManyToManyField[Any, Any]
    included_categories: models.ManyToManyField[Any, Any]
    excluded_categories: models.ManyToManyField[Any, Any]

    proxy_class: models.CharField[str | Combinable | None, str | None]
    date_created: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]

    objects: ClassVar[models.Manager[AbstractRange]]
    browsable: ClassVar[models.Manager[AbstractRange]]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    def get_absolute_url(self) -> str: ...
    @property
    def proxy(self) -> Any | None: ...
    def add_product(self, product: Any, display_order: int | None = ...) -> None: ...
    def remove_product(self, product: Any) -> None: ...
    def contains_product(self, product: Any) -> bool: ...
    def invalidate_cached_queryset(self) -> None: ...
    def num_products(self) -> int | None: ...
    def all_products(self) -> QuerySet[Any]: ...
    @property
    def product_queryset(self) -> QuerySet[Any]: ...
    @property
    def is_editable(self) -> bool: ...
    @property
    def is_reorderable(self) -> bool: ...

class AbstractRangeProduct(models.Model):
    range: models.ForeignKey[Any | Combinable, Any]
    product: models.ForeignKey[Any | Combinable, Any]
    display_order: models.IntegerField[int | Combinable, int]

    class Meta:
        abstract: bool
        app_label: str
        unique_together: tuple[str, ...]

class AbstractRangeProductFileUpload(models.Model):
    range: models.ForeignKey[Any | Combinable, Any]
    filepath: models.CharField[str | Combinable, str]
    size: models.PositiveIntegerField[int | Combinable, int]
    uploaded_by: models.ForeignKey[Any | Combinable, Any]
    date_uploaded: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]

    INCLUDED_PRODUCTS_TYPE: ClassVar[str]
    EXCLUDED_PRODUCTS_TYPE: ClassVar[str]
    UPLOAD_TYPE_CHOICES: ClassVar[list[tuple[str, str]]]
    upload_type: models.CharField[str | Combinable, str]

    PENDING: ClassVar[str]
    FAILED: ClassVar[str]
    PROCESSED: ClassVar[str]
    choices: ClassVar[tuple[tuple[str, str], ...]]

    status: models.CharField[str | Combinable, str]
    error_message: models.CharField[str | Combinable, str]

    date_processed: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]
    num_new_skus: models.PositiveIntegerField[int | Combinable | None, int | None]
    num_unknown_skus: models.PositiveIntegerField[int | Combinable | None, int | None]
    num_duplicate_skus: models.PositiveIntegerField[int | Combinable | None, int | None]

    class Meta:
        abstract: bool
        app_label: str
        ordering: tuple[str, ...]
        verbose_name: str
        verbose_name_plural: str

    def mark_as_failed(self, message: str | None = ...) -> None: ...
    def mark_as_processed(self, num_new: int, num_unknown: int, num_duplicate: int) -> None: ...
    def was_processing_successful(self) -> bool: ...
    def process(self, file_obj: IOBase) -> QuerySet[Any]: ...
    def extract_ids(self, file_obj: IOBase) -> Any: ...
