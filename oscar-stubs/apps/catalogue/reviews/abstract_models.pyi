from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import Combinable
from oscar.models.fields import NullCharField

class AbstractProductReview(models.Model):
    product: models.ForeignKey[Any | None | Combinable, Any | None]
    SCORE_CHOICES: ClassVar[tuple[tuple[int, int], ...]]
    score: models.SmallIntegerField
    title: models.CharField
    body: models.TextField
    user: models.ForeignKey[User | None | Combinable, User | None]
    name: models.CharField
    email: models.EmailField
    homepage: models.URLField
    FOR_MODERATION: ClassVar[int]
    APPROVED: ClassVar[int]
    REJECTED: ClassVar[int]
    STATUS_CHOICES: ClassVar[tuple[tuple[int, str], ...]]
    status: models.SmallIntegerField
    code: NullCharField
    total_votes: models.IntegerField
    delta_votes: models.IntegerField
    date_created: models.DateTimeField

    objects: ClassVar[models.Manager[AbstractProductReview]]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        unique_together: tuple[tuple[str, str], ...]
        verbose_name: str
        verbose_name_plural: str

    def get_absolute_url(self) -> str: ...
    def clean(self) -> None: ...
    def vote_up(self, user: User) -> None: ...
    def vote_down(self, user: User) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]: ...
    @property
    def is_anonymous(self) -> bool: ...
    @property
    def pending_moderation(self) -> bool: ...
    @property
    def is_approved(self) -> bool: ...
    @property
    def is_rejected(self) -> bool: ...
    @property
    def has_votes(self) -> bool: ...
    @property
    def num_up_votes(self) -> int: ...
    @property
    def num_down_votes(self) -> int: ...
    @property
    def reviewer_name(self) -> str: ...
    def update_totals(self) -> None: ...
    def can_user_vote(self, user: User) -> tuple[bool, str]: ...

class AbstractVote(models.Model):
    review: models.ForeignKey[Any | Combinable, Any]
    user: models.ForeignKey[User | Combinable, User]
    UP: ClassVar[int]
    DOWN: ClassVar[int]
    VOTE_CHOICES: ClassVar[tuple[tuple[int, str], ...]]
    delta: models.SmallIntegerField
    date_created: models.DateTimeField

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        unique_together: tuple[tuple[str, str], ...]
        verbose_name: str
        verbose_name_plural: str

    def clean(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
