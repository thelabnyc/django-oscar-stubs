from oscar.apps.catalogue.reviews.abstract_models import (
    AbstractProductReview as AbstractProductReview,
)
from oscar.apps.catalogue.reviews.abstract_models import (
    AbstractVote as AbstractVote,
)

class ProductReview(AbstractProductReview):
    id: int

class Vote(AbstractVote):
    id: int
