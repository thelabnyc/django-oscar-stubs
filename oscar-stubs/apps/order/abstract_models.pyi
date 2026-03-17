from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.expressions import Combinable
from oscar.apps.address.abstract_models import AbstractBillingAddress, AbstractShippingAddress
from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.catalogue.abstract_models import AbstractOption, AbstractProduct
from oscar.apps.communication.abstract_models import AbstractCommunicationEventType
from oscar.apps.offer.abstract_models import AbstractConditionalOffer
from oscar.apps.partner.abstract_models import AbstractPartner, AbstractStockRecord
from oscar.apps.voucher.abstract_models import AbstractVoucher
from oscar.models.fields import AutoSlugField

class AbstractOrder(models.Model):
    # Fields
    number: models.CharField[str | Combinable, str]
    site: models.ForeignKey[Site | Combinable | None, Site | None]
    site_id: int | None
    basket: models.ForeignKey[AbstractBasket | Combinable | None, AbstractBasket | None]
    basket_id: int | None
    user: models.ForeignKey[User | Combinable | None, User | None]
    user_id: int | None
    billing_address: models.ForeignKey[AbstractBillingAddress | Combinable | None, AbstractBillingAddress | None]
    billing_address_id: int | None
    currency: models.CharField[str | Combinable, str]
    total_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    total_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    shipping_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    shipping_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    shipping_tax_code: models.CharField[str | Combinable | None, str | None]
    shipping_address: models.ForeignKey[AbstractShippingAddress | Combinable | None, AbstractShippingAddress | None]
    shipping_address_id: int | None
    shipping_method: models.CharField[str | Combinable, str]
    shipping_code: models.CharField[str | Combinable, str]
    status: models.CharField[str | Combinable, str]
    guest_email: models.EmailField[str | Combinable, str]
    date_placed: models.DateTimeField[str | datetime | Combinable, datetime]
    analytics_tracked: models.BooleanField[bool | Combinable, bool]

    # Class-level pipeline settings
    pipeline: ClassVar[dict[str, list[str] | tuple[str, ...]]]
    cascade: ClassVar[dict[str, str]]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

    def save(self, *args: Any, **kwargs: Any) -> None: ...

    # Status methods
    @classmethod
    def all_statuses(cls) -> list[str]: ...
    def available_statuses(self) -> list[str] | tuple[str, ...]: ...
    def set_status(self, new_status: str) -> None: ...
    def _create_order_status_change(self, old_status: str, new_status: str) -> None: ...

    # Properties
    @property
    def is_anonymous(self) -> bool: ...
    @property
    def basket_total_before_discounts_incl_tax(self) -> Decimal: ...
    @property
    def basket_total_before_discounts_excl_tax(self) -> Decimal: ...
    @property
    def basket_total_incl_tax(self) -> Decimal: ...
    @property
    def basket_total_excl_tax(self) -> Decimal: ...
    @property
    def total_before_discounts_incl_tax(self) -> Decimal: ...
    @property
    def total_before_discounts_excl_tax(self) -> Decimal: ...
    @property
    def total_discount_incl_tax(self) -> Decimal: ...
    @property
    def total_discount_excl_tax(self) -> Decimal: ...
    @property
    def total_tax(self) -> Decimal: ...
    @property
    def surcharge_excl_tax(self) -> Decimal: ...
    @property
    def surcharge_incl_tax(self) -> Decimal: ...
    @property
    def num_lines(self) -> int: ...
    @property
    def num_items(self) -> int: ...
    @property
    def shipping_tax(self) -> Decimal: ...
    @property
    def shipping_status(self) -> str: ...
    @property
    def has_shipping_discounts(self) -> bool: ...
    @property
    def shipping_before_discounts_incl_tax(self) -> Decimal: ...
    @property
    def email(self) -> str: ...
    @property
    def basket_discounts(self) -> models.QuerySet[AbstractOrderDiscount]: ...
    @property
    def shipping_discounts(self) -> models.QuerySet[AbstractOrderDiscount]: ...
    @property
    def post_order_actions(self) -> models.QuerySet[AbstractOrderDiscount]: ...
    def _is_event_complete(self, event_quantities: list[Any]) -> bool: ...
    def verification_hash(self) -> str: ...
    def check_verification_hash(self, hash_to_check: str) -> bool: ...
    def set_date_placed_default(self) -> None: ...

class AbstractOrderNote(models.Model):
    # Constants
    INFO: ClassVar[str]
    WARNING: ClassVar[str]
    ERROR: ClassVar[str]
    SYSTEM: ClassVar[str]

    editable_lifetime: ClassVar[int]

    # Fields
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    user: models.ForeignKey[User | Combinable | None, User | None]
    user_id: int | None
    note_type: models.CharField[str | Combinable, str]
    message: models.TextField[str | Combinable, str]
    date_created: models.DateTimeField[str | datetime | Combinable, datetime]
    date_updated: models.DateTimeField[str | datetime | Combinable, datetime]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

    def is_editable(self) -> bool: ...

class AbstractOrderStatusChange(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    old_status: models.CharField[str | Combinable, str]
    new_status: models.CharField[str | Combinable, str]
    date_created: models.DateTimeField[str | datetime | Combinable, datetime]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[list[str]]

class AbstractCommunicationEvent(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    event_type: models.ForeignKey[AbstractCommunicationEventType | Combinable, AbstractCommunicationEventType]
    event_type_id: int
    date_created: models.DateTimeField[str | datetime | Combinable, datetime]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[list[str]]

class AbstractLine(models.Model):
    # Fields
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    partner: models.ForeignKey[AbstractPartner | Combinable | None, AbstractPartner | None]
    partner_id: int | None
    partner_name: models.CharField[str | Combinable, str]
    partner_sku: models.CharField[str | Combinable, str]
    partner_line_reference: models.CharField[str | Combinable, str]
    partner_line_notes: models.TextField[str | Combinable, str]
    stockrecord: models.ForeignKey[AbstractStockRecord | Combinable | None, AbstractStockRecord | None]
    stockrecord_id: int | None
    product: models.ForeignKey[AbstractProduct | Combinable | None, AbstractProduct | None]
    product_id: int | None
    title: models.CharField[str | Combinable, str]
    upc: models.CharField[str | Combinable | None, str | None]
    quantity: models.PositiveIntegerField[float | Combinable, int]
    line_price_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    line_price_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    line_price_before_discounts_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    line_price_before_discounts_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    unit_price_incl_tax: models.DecimalField[str | Decimal | Combinable | None, Decimal | None]
    unit_price_excl_tax: models.DecimalField[str | Decimal | Combinable | None, Decimal | None]
    tax_code: models.CharField[str | Combinable | None, str | None]
    status: models.CharField[str | Combinable, str]
    num_allocated: models.PositiveIntegerField[float | Combinable, int]
    allocation_cancelled: models.BooleanField[bool | Combinable, bool]

    # Class-level pipeline
    pipeline: ClassVar[dict[str, list[str] | tuple[str, ...]]]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

    # Status methods
    @classmethod
    def all_statuses(cls) -> list[str]: ...
    def available_statuses(self) -> list[str] | tuple[str, ...]: ...
    def set_status(self, new_status: str) -> None: ...

    # Properties
    @property
    def description(self) -> str: ...
    @property
    def discount_incl_tax(self) -> Decimal: ...
    @property
    def discount_excl_tax(self) -> Decimal: ...
    @property
    def line_price_tax(self) -> Decimal: ...
    @property
    def unit_price_tax(self) -> Decimal: ...
    @property
    def shipping_status(self) -> str: ...
    @property
    def shipping_event_breakdown(self) -> dict[str, dict[str, Any]]: ...
    @property
    def is_product_deleted(self) -> bool: ...
    @property
    def can_track_allocations(self) -> bool: ...

    # Shipping event methods
    def is_shipping_event_permitted(self, event_type: Any, quantity: int) -> bool: ...
    def shipping_event_quantity(self, event_type: Any) -> int: ...
    def has_shipping_event_occurred(self, event_type: Any, quantity: int | None = ...) -> bool: ...
    def get_event_quantity(self, event: Any) -> Any: ...

    # Payment event methods
    def is_payment_event_permitted(self, event_type: Any, quantity: int) -> bool: ...
    def payment_event_quantity(self, event_type: Any) -> int: ...

    # Reorder
    def is_available_to_reorder(self, basket: Any, strategy: Any) -> tuple[bool, str | None]: ...

    # Allocation methods
    def is_allocation_consumption_possible(self, quantity: int) -> bool: ...
    def consume_allocation(self, quantity: int) -> None: ...
    def cancel_allocation(self, quantity: int) -> None: ...

class AbstractLineAttribute(models.Model):
    line: models.ForeignKey[AbstractLine | Combinable, AbstractLine]
    line_id: int
    option: models.ForeignKey[AbstractOption | Combinable | None, AbstractOption | None]
    option_id: int | None
    type: models.CharField[str | Combinable, str]
    value: models.JSONField[Any, Any]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

class AbstractLinePrice(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    line: models.ForeignKey[AbstractLine | Combinable, AbstractLine]
    line_id: int
    quantity: models.PositiveIntegerField[float | Combinable, int]
    price_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    price_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    shipping_incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    shipping_excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    tax_code: models.CharField[str | Combinable | None, str | None]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[tuple[str, ...]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

class AbstractPaymentEventType(models.Model):
    name: models.CharField[str | Combinable, str]
    code: AutoSlugField

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[tuple[str, ...]]

class AbstractPaymentEvent(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    amount: models.DecimalField[str | Decimal | Combinable, Decimal]
    reference: models.CharField[str | Combinable, str]
    lines: models.ManyToManyField[AbstractLine, AbstractLine]
    event_type: models.ForeignKey[AbstractPaymentEventType | Combinable, AbstractPaymentEventType]
    event_type_id: int
    shipping_event: models.ForeignKey[AbstractShippingEvent | Combinable | None, AbstractShippingEvent | None]
    shipping_event_id: int | None
    date_created: models.DateTimeField[str | datetime | Combinable, datetime]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[list[str]]

    def num_affected_lines(self) -> int: ...

class PaymentEventQuantity(models.Model):
    id: int
    event: models.ForeignKey[AbstractPaymentEvent | Combinable, AbstractPaymentEvent]
    event_id: int
    line: models.ForeignKey[AbstractLine | Combinable, AbstractLine]
    line_id: int
    quantity: models.PositiveIntegerField[float | Combinable, int]

    class Meta:
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        unique_together: ClassVar[tuple[str, ...]]

class AbstractShippingEvent(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    lines: models.ManyToManyField[AbstractLine, AbstractLine]
    event_type: models.ForeignKey[AbstractShippingEventType | Combinable, AbstractShippingEventType]
    event_type_id: int
    notes: models.TextField[str | Combinable, str]
    date_created: models.DateTimeField[str | datetime | Combinable, datetime]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[list[str]]

    def num_affected_lines(self) -> int: ...

class ShippingEventQuantity(models.Model):
    id: int
    event: models.ForeignKey[AbstractShippingEvent | Combinable, AbstractShippingEvent]
    event_id: int
    line: models.ForeignKey[AbstractLine | Combinable, AbstractLine]
    line_id: int
    quantity: models.PositiveIntegerField[float | Combinable, int]

    class Meta:
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        unique_together: ClassVar[tuple[str, ...]]

    def save(self, *args: Any, **kwargs: Any) -> None: ...

class AbstractShippingEventType(models.Model):
    name: models.CharField[str | Combinable, str]
    code: AutoSlugField

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
        ordering: ClassVar[tuple[str, ...]]

class AbstractOrderDiscount(models.Model):
    # Category constants
    BASKET: ClassVar[str]
    SHIPPING: ClassVar[str]
    DEFERRED: ClassVar[str]
    CATEGORY_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    # Fields
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    category: models.CharField[str | Combinable, str]
    offer_id: models.PositiveIntegerField[float | Combinable | None, int | None]
    offer_name: models.CharField[str | Combinable, str]
    voucher_id: models.PositiveIntegerField[float | Combinable | None, int | None]
    voucher_code: models.CharField[str | Combinable, str]
    frequency: models.PositiveIntegerField[float | Combinable | None, int | None]
    amount: models.DecimalField[str | Decimal | Combinable, Decimal]
    message: models.TextField[str | Combinable, str]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def get_category_display(self) -> str: ...
    def description(self) -> str: ...
    @property
    def is_basket_discount(self) -> bool: ...
    @property
    def is_shipping_discount(self) -> bool: ...
    @property
    def is_post_order_action(self) -> bool: ...
    @property
    def offer(self) -> AbstractConditionalOffer | None: ...
    @property
    def voucher(self) -> AbstractVoucher | None: ...

class AbstractOrderLineDiscount(models.Model):
    line: models.ForeignKey[AbstractLine | Combinable, AbstractLine]
    line_id: int
    order_discount: models.ForeignKey[AbstractOrderDiscount | Combinable, AbstractOrderDiscount]
    order_discount_id: int
    is_incl_tax: models.BooleanField[bool | Combinable, bool]
    amount: models.DecimalField[str | Decimal | Combinable, Decimal]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]

class AbstractSurcharge(models.Model):
    order: models.ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    name: models.CharField[str | Combinable, str]
    code: models.CharField[str | Combinable, str]
    incl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    excl_tax: models.DecimalField[str | Decimal | Combinable, Decimal]
    tax_code: models.CharField[str | Combinable | None, str | None]

    @property
    def tax(self) -> Decimal: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        verbose_name: ClassVar[str]
        verbose_name_plural: ClassVar[str]
