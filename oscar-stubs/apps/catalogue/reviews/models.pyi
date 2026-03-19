from typing import ClassVar

from django.db import models
from oscar.apps.catalogue.reviews.abstract_models import (
    AbstractProductReview as AbstractProductReview,
)
from oscar.apps.catalogue.reviews.abstract_models import (
    AbstractVote as AbstractVote,
)

class ProductReview(AbstractProductReview):
    id: int
    objects: ClassVar[models.Manager[ProductReview]]  # type: ignore[assignment]

class Vote(AbstractVote):
    id: int
