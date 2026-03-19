from decimal import Decimal
from io import IOBase
from typing import Any, ClassVar
import builtins
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import Combinable
from django.db.models.query import QuerySet
from django.utils.functional import _StrPromise
from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.basket.abstract_models import AbstractLine as AbstractBasketLine
from oscar.apps.catalogue.abstract_models import AbstractCategory, AbstractProduct, AbstractProductClass
from oscar.apps.offer.results import ApplicationResult, OfferApplication
from oscar.apps.voucher.abstract_models import AbstractVoucher

class BaseOfferMixin(models.Model):
    class Meta:
        abstract: bool

    def proxy(self) -> BaseOfferMixin: ...
    @property
    def name(self) -> str | _StrPromise: ...
    @property
    def description(self) -> str | _StrPromise | None: ...

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
    combinations: models.ManyToManyField[AbstractConditionalOffer, AbstractConditionalOffer]

    # Status constants
    OPEN: ClassVar[str]
    SUSPENDED: ClassVar[str]
    CONSUMED: ClassVar[str]

    status: models.CharField[str | Combinable, str]

    condition: models.ForeignKey[AbstractCondition | Combinable, AbstractCondition]
    condition_id: int
    benefit: models.ForeignKey[AbstractBenefit | Combinable, AbstractBenefit]
    benefit_id: int

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
    def is_available(self, user: User | None = ..., test_date: datetime.datetime | None = ...) -> bool: ...
    def is_condition_satisfied(self, basket: AbstractBasket) -> bool: ...
    def is_condition_partially_satisfied(self, basket: AbstractBasket) -> bool: ...
    def get_upsell_message(self, basket: AbstractBasket) -> str | None: ...
    def apply_benefit(self, basket: AbstractBasket) -> ApplicationResult: ...
    def apply_deferred_benefit(self, basket: AbstractBasket, order: Any, application: dict[str, Any]) -> Any: ...
    def set_voucher(self, voucher: AbstractVoucher) -> None: ...
    def get_voucher(self) -> AbstractVoucher | None: ...
    def get_max_applications(self, user: User | None = ...) -> int: ...
    def get_num_user_applications(self, user: User) -> int: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...
    def record_usage(self, discount: OfferApplication) -> None: ...
    def availability_description(self) -> str: ...
    def availability_restrictions(self) -> list[dict[str, Any]]: ...
    @property
    def has_products(self) -> bool: ...
    def products(self) -> QuerySet[AbstractProduct]: ...
    @property
    def combined_offers(self) -> QuerySet[AbstractConditionalOffer]: ...
    def get_offer_type_display(self) -> str: ...

class AbstractBenefit(BaseOfferMixin, models.Model):
    range: models.ForeignKey[AbstractRange | None | Combinable, AbstractRange | None]
    range_id: int | None

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
    def proxy_map(self) -> dict[str, builtins.type]: ...
    def apply(
        self, basket: AbstractBasket, condition: AbstractCondition, offer: AbstractConditionalOffer
    ) -> ApplicationResult: ...
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
    def can_apply_benefit(self, line: AbstractBasketLine) -> bool: ...
    def get_applicable_lines(
        self, offer: AbstractConditionalOffer, basket: AbstractBasket, range: AbstractRange | None = ...
    ) -> list[tuple[Decimal, AbstractBasketLine]]: ...
    def shipping_discount(self, charge: Decimal, currency: str | None = ...) -> Decimal: ...
    def get_type_display(self) -> str: ...

class AbstractCondition(BaseOfferMixin, models.Model):
    COUNT: ClassVar[str]
    VALUE: ClassVar[str]
    COVERAGE: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    range: models.ForeignKey[AbstractRange | None | Combinable, AbstractRange | None]
    range_id: int | None
    type: models.CharField[str | Combinable, str]
    value: models.DecimalField[Decimal | str | Combinable | None, Decimal | None]
    proxy_class: models.CharField[str | Combinable | None, str | None]

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

    @property
    def proxy_map(self) -> dict[str, builtins.type]: ...
    def clean(self) -> None: ...
    def clean_count(self) -> None: ...
    def clean_value(self) -> None: ...
    def clean_coverage(self) -> None: ...
    def consume_items(
        self,
        offer: AbstractConditionalOffer,
        basket: AbstractBasket,
        affected_lines: list[tuple[AbstractBasketLine, Decimal, int]],
    ) -> list[tuple[AbstractBasketLine, Decimal, int]] | None: ...
    def is_satisfied(self, offer: AbstractConditionalOffer, basket: AbstractBasket) -> bool: ...
    def is_partially_satisfied(self, offer: AbstractConditionalOffer, basket: AbstractBasket) -> bool: ...
    def get_upsell_message(
        self, offer: AbstractConditionalOffer, basket: AbstractBasket
    ) -> str | _StrPromise | None: ...
    def can_apply_condition(self, line: AbstractBasketLine) -> bool: ...
    def get_applicable_lines(
        self, offer: AbstractConditionalOffer, basket: AbstractBasket, most_expensive_first: bool = ...
    ) -> list[tuple[Decimal, AbstractBasketLine]]: ...
    def get_type_display(self) -> str: ...

class AbstractRange(models.Model):
    name: models.CharField[str | Combinable, str]
    slug: models.CharField[str | Combinable, str]
    description: models.TextField[str | Combinable, str]
    is_public: models.BooleanField[bool | Combinable, bool]
    includes_all_products: models.BooleanField[bool | Combinable, bool]

    included_products: models.ManyToManyField[AbstractProduct, AbstractProduct]
    excluded_products: models.ManyToManyField[AbstractProduct, AbstractProduct]
    classes: models.ManyToManyField[AbstractProductClass, AbstractProductClass]
    included_categories: models.ManyToManyField[AbstractCategory, AbstractCategory]
    excluded_categories: models.ManyToManyField[AbstractCategory, AbstractCategory]

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
    def add_product(self, product: AbstractProduct, display_order: int | None = ...) -> None: ...
    def remove_product(self, product: AbstractProduct) -> None: ...
    def contains_product(self, product: AbstractProduct) -> bool: ...
    def invalidate_cached_queryset(self) -> None: ...
    def num_products(self) -> int | None: ...
    def all_products(self) -> QuerySet[AbstractProduct]: ...
    @property
    def product_queryset(self) -> QuerySet[AbstractProduct]: ...
    @property
    def is_editable(self) -> bool: ...
    @property
    def is_reorderable(self) -> bool: ...

class AbstractRangeProduct(models.Model):
    range: models.ForeignKey[AbstractRange | Combinable, AbstractRange]
    range_id: int
    product: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    display_order: models.IntegerField[int | Combinable, int]

    class Meta:
        abstract: bool
        app_label: str
        unique_together: tuple[str, ...]

class AbstractRangeProductFileUpload(models.Model):
    range: models.ForeignKey[AbstractRange | Combinable, AbstractRange]
    range_id: int
    filepath: models.CharField[str | Combinable, str]
    size: models.PositiveIntegerField[int | Combinable, int]
    uploaded_by: models.ForeignKey[User | Combinable, User]
    uploaded_by_id: int
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
    def get_status_display(self) -> str: ...
    def get_upload_type_display(self) -> str: ...
    def process(self, file_obj: IOBase) -> QuerySet[Any]: ...
    def extract_ids(self, file_obj: IOBase) -> Any: ...
