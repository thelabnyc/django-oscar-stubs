from typing import Any, ClassVar

from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from oscar.apps.communication.managers import CommunicationTypeManager
from oscar.models.fields import AutoSlugField

class AbstractEmail(models.Model):
    user: ForeignKey[Any | None | Combinable, Any | None]
    email: models.EmailField[str | None | Combinable, str | None]
    subject: models.TextField[str | Combinable, str]
    body_text: models.TextField[str | Combinable, str]
    body_html: models.TextField[str | Combinable, str]
    date_sent: models.DateTimeField[str | Combinable, Any]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractCommunicationEventType(models.Model):
    ORDER_RELATED: ClassVar[str]
    USER_RELATED: ClassVar[str]
    CATEGORY_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    code: AutoSlugField
    name: models.CharField[str | int | Combinable, str]
    category: models.CharField[str | int | Combinable, str]
    email_subject_template: models.CharField[str | int | None | Combinable, str | None]
    email_body_template: models.TextField[str | None | Combinable, str | None]
    email_body_html_template: models.TextField[str | None | Combinable, str | None]
    sms_template: models.CharField[str | int | None | Combinable, str | None]
    date_created: models.DateTimeField[str | Combinable, Any]
    date_updated: models.DateTimeField[str | Combinable, Any]

    objects: ClassVar[CommunicationTypeManager]

    email_subject_template_file: ClassVar[str]
    email_body_template_file: ClassVar[str]
    email_body_html_template_file: ClassVar[str]
    sms_template_file: ClassVar[str]

    def get_messages(self, ctx: dict[str, Any] | None = ...) -> dict[str, str]: ...
    def is_order_related(self) -> bool: ...
    def is_user_related(self) -> bool: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class AbstractNotification(models.Model):
    INBOX: ClassVar[str]
    ARCHIVE: ClassVar[str]
    choices: ClassVar[tuple[tuple[str, str], ...]]

    recipient: ForeignKey[Any | Combinable, Any]
    sender: ForeignKey[Any | None | Combinable, Any | None]
    subject: models.CharField[str | int | Combinable, str]
    body: models.TextField[str | Combinable, str]
    location: models.CharField[str | int | Combinable, str]
    date_sent: models.DateTimeField[str | Combinable, Any]
    date_read: models.DateTimeField[str | None | Combinable, Any | None]

    def archive(self) -> None: ...
    @property
    def is_read(self) -> bool: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: tuple[str, ...]
        verbose_name: str
        verbose_name_plural: str
