from datetime import date
from decimal import Decimal
from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from oscar.apps.order.abstract_models import AbstractOrder
from oscar.models.fields import AutoSlugField

class AbstractTransaction(models.Model):
    AUTHORISE: ClassVar[str]
    DEBIT: ClassVar[str]
    REFUND: ClassVar[str]

    source: ForeignKey[AbstractSource | Combinable, AbstractSource]
    source_id: int
    txn_type: models.CharField[str | int | Combinable, str]
    amount: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    reference: models.CharField[str | int | Combinable, str]
    status: models.CharField[str | int | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractSource(models.Model):
    order: ForeignKey[AbstractOrder | Combinable, AbstractOrder]
    order_id: int
    source_type: ForeignKey[AbstractSourceType | Combinable, AbstractSourceType]
    source_type_id: int
    currency: models.CharField[str | int | Combinable, str]
    amount_allocated: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    amount_debited: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    amount_refunded: models.DecimalField[str | float | Decimal | Combinable, Decimal]
    reference: models.CharField[str | int | Combinable, str]
    label: models.CharField[str | int | Combinable, str]

    submission_data: dict[str, Any] | None
    deferred_txns: list[tuple[str, Decimal, str, str]] | None

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def create_deferred_transaction(
        self, txn_type: str, amount: Decimal, reference: str = ..., status: str = ...
    ) -> None: ...
    def _create_transaction(self, txn_type: str, amount: Decimal, reference: str = ..., status: str = ...) -> None: ...
    def allocate(self, amount: Decimal, reference: str = ..., status: str = ...) -> None: ...
    def debit(self, amount: Decimal | None = ..., reference: str = ..., status: str = ...) -> None: ...
    def refund(self, amount: Decimal, reference: str = ..., status: str = ...) -> None: ...
    @property
    def balance(self) -> Decimal: ...
    @property
    def amount_available_for_refund(self) -> Decimal: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractSourceType(models.Model):
    name: models.CharField[str | int | Combinable, str]
    code: AutoSlugField

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractBankcard(models.Model):
    user: ForeignKey[User | Combinable, User]
    user_id: int
    card_type: models.CharField[str | int | Combinable, str]
    name: models.CharField[str | int | Combinable, str]
    number: models.CharField[str | int | Combinable, str]
    expiry_date: models.DateField[str | date | Combinable, date]
    partner_reference: models.CharField[str | int | Combinable, str]

    start_date: date | None
    issue_number: str | None
    ccv: str | None

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def prepare_for_save(self) -> None: ...
    @property
    def cvv(self) -> str | None: ...
    @property
    def obfuscated_number(self) -> str: ...
    def start_month(self, format: str = ...) -> str: ...
    def expiry_month(self, format: str = ...) -> str: ...

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str
