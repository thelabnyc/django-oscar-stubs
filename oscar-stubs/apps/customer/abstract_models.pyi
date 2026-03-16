from typing import Any, ClassVar
import datetime

from django.contrib.auth import models as auth_models
from django.db import models
from django.db.models.expressions import Combinable

class UserManager(auth_models.BaseUserManager["AbstractUser"]):
    def create_user(self, email: str, password: str | None = ..., **extra_fields: Any) -> AbstractUser: ...
    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> AbstractUser: ...

class AbstractUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email: models.EmailField[str | Combinable, str]
    first_name: models.CharField[str | Combinable, str]
    last_name: models.CharField[str | Combinable, str]
    is_staff: models.BooleanField[bool | Combinable, bool]
    is_active: models.BooleanField[bool | Combinable, bool]
    date_joined: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]

    objects: ClassVar[UserManager]

    USERNAME_FIELD: ClassVar[str]

    class Meta:
        abstract: bool
        verbose_name: str
        verbose_name_plural: str

    def clean(self) -> None: ...
    def get_full_name(self) -> str: ...
    def get_short_name(self) -> str: ...
    def email_user(self, subject: str, message: str, from_email: str | None = ..., **kwargs: Any) -> None: ...
    def _migrate_alerts_to_user(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...

class AbstractProductAlert(models.Model):
    product: models.ForeignKey[Any | Combinable, Any]
    user: models.ForeignKey[Any | Combinable | None, Any | None]
    email: models.EmailField[str | Combinable, str]
    key: models.CharField[str | Combinable, str]

    UNCONFIRMED: ClassVar[str]
    ACTIVE: ClassVar[str]
    CANCELLED: ClassVar[str]
    CLOSED: ClassVar[str]
    STATUS_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    status: models.CharField[str | Combinable, str]

    date_created: models.DateTimeField[str | datetime.datetime | Combinable, datetime.datetime]
    date_confirmed: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]
    date_cancelled: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]
    date_closed: models.DateTimeField[str | datetime.datetime | Combinable | None, datetime.datetime | None]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    @property
    def is_anonymous(self) -> bool: ...
    @property
    def can_be_confirmed(self) -> bool: ...
    @property
    def can_be_cancelled(self) -> bool: ...
    @property
    def is_cancelled(self) -> bool: ...
    @property
    def is_active(self) -> bool: ...
    def confirm(self) -> None: ...
    def cancel(self) -> None: ...
    def close(self) -> None: ...
    def get_email_address(self) -> str: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def get_random_key(self) -> str: ...
    def get_confirm_url(self) -> str: ...
    def get_cancel_url(self) -> str: ...
