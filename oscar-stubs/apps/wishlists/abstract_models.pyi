from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.expressions import Combinable
from django.utils.functional import _StrPromise
from oscar.apps.catalogue.abstract_models import AbstractProduct

class AbstractWishList(models.Model):
    PUBLIC: ClassVar[str]
    PRIVATE: ClassVar[str]
    SHARED: ClassVar[str]
    VISIBILITY_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    owner: ForeignKey[User | Combinable, User]
    owner_id: int
    name: models.CharField[str | int | Combinable, str]
    key: models.CharField[str | int | Combinable, str]
    visibility: models.CharField[str | int | Combinable, str]
    date_created: models.DateTimeField[str | Combinable, Any]

    def save(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def random_key(cls, length: int = ...) -> str: ...
    def is_allowed_to_see(self, user: Any) -> bool: ...
    def is_allowed_to_edit(self, user: Any) -> bool: ...
    def get_absolute_url(self) -> str: ...
    def add(self, product: Any) -> None: ...
    def get_shared_url(self) -> str: ...
    @property
    def is_shareable(self) -> bool: ...
    def get_visibility_display(self) -> str: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[tuple[str, ...]]
        verbose_name: ClassVar[str | _StrPromise]

class AbstractLine(models.Model):
    wishlist: ForeignKey[AbstractWishList | Combinable, AbstractWishList]
    wishlist_id: int
    product: ForeignKey[AbstractProduct | None | Combinable, AbstractProduct | None]
    product_id: int | None
    quantity: models.PositiveIntegerField[float | int | str | Combinable, int]
    title: models.CharField[str | int | Combinable, str]

    def get_title(self) -> str: ...

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        ordering: ClassVar[list[str]]
        unique_together: ClassVar[tuple[tuple[str, str], ...]]
        verbose_name: ClassVar[str | _StrPromise]

class AbstractWishListSharedEmail(models.Model):
    wishlist: ForeignKey[AbstractWishList | Combinable, AbstractWishList]
    wishlist_id: int
    email: models.EmailField[str | Combinable, str]

    class Meta:
        abstract: ClassVar[bool]
        app_label: ClassVar[str]
        verbose_name: ClassVar[str | _StrPromise]
