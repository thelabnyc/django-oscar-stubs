from typing import Any, ClassVar

from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from oscar.models.fields import NullCharField, UppercaseCharField

class AbstractAddress(models.Model):
    MR: ClassVar[str]
    MISS: ClassVar[str]
    MRS: ClassVar[str]
    MS: ClassVar[str]
    DR: ClassVar[str]
    TITLE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    POSTCODE_REQUIRED: ClassVar[bool]
    POSTCODES_REGEX: ClassVar[dict[str, str]]

    code: NullCharField
    title: models.CharField[str | int | Combinable, str]
    first_name: models.CharField[str | int | Combinable, str]
    last_name: models.CharField[str | int | Combinable, str]
    line1: models.CharField[str | int | Combinable, str]
    line2: models.CharField[str | int | Combinable, str]
    line3: models.CharField[str | int | Combinable, str]
    line4: models.CharField[str | int | Combinable, str]
    state: models.CharField[str | int | Combinable, str]
    postcode: UppercaseCharField
    country: ForeignKey[Any | Combinable, Any]
    search_text: models.TextField[str | Combinable, str]

    search_fields: ClassVar[list[str]]
    base_fields: ClassVar[list[str]]
    hash_fields: ClassVar[list[str]]

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def clean(self) -> None: ...
    def ensure_postcode_is_valid_for_country(self) -> None: ...
    def _update_search_text(self) -> None: ...
    @property
    def city(self) -> str: ...
    @property
    def summary(self) -> str: ...
    @property
    def salutation(self) -> str: ...
    @property
    def name(self) -> str: ...
    def get_field_values(self, fields: list[str] | tuple[str, ...]) -> list[Any]: ...
    def get_address_field_values(self, fields: list[str]) -> list[str]: ...
    def generate_hash(self) -> int: ...
    def join_fields(self, fields: list[str] | tuple[str, ...], separator: str = ...) -> str: ...
    def populate_alternative_model(self, address_model: models.Model) -> None: ...
    def active_address_fields(self) -> list[str]: ...

    class Meta:
        abstract: bool
        verbose_name: str
        verbose_name_plural: str

class AbstractCountry(models.Model):
    iso_3166_1_a2: models.CharField[str | int | Combinable, str]
    iso_3166_1_a3: models.CharField[str | int | Combinable, str]
    iso_3166_1_numeric: models.CharField[str | int | Combinable, str]
    printable_name: models.CharField[str | int | Combinable, str]
    name: models.CharField[str | int | Combinable, str]
    display_order: models.PositiveSmallIntegerField[float | int | str | Combinable, int]
    is_shipping_country: models.BooleanField[bool | Combinable, bool]

    @property
    def code(self) -> str: ...
    @property
    def numeric_code(self) -> str: ...

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str
        ordering: tuple[str, ...]

class AbstractShippingAddress(AbstractAddress):
    phone_number: Any  # PhoneNumberField
    notes: models.TextField[str | Combinable, str]

    @property
    def order(self) -> Any: ...

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

class AbstractUserAddress(AbstractShippingAddress):
    user: ForeignKey[Any | Combinable, Any]
    is_default_for_shipping: models.BooleanField[bool | Combinable, bool]
    is_default_for_billing: models.BooleanField[bool | Combinable, bool]
    num_orders_as_shipping_address: models.PositiveIntegerField[float | int | str | Combinable, int]
    num_orders_as_billing_address: models.PositiveIntegerField[float | int | str | Combinable, int]
    hash: models.CharField[str | int | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def _ensure_defaults_integrity(self) -> None: ...
    def validate_unique(self, exclude: Any = ...) -> None: ...

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str
        ordering: list[str]
        unique_together: tuple[str, ...]

class AbstractBillingAddress(AbstractAddress):
    @property
    def order(self) -> Any: ...

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

class AbstractPartnerAddress(AbstractAddress):
    partner: ForeignKey[Any | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str
