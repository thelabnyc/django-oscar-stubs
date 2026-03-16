from typing import Any

from django.db import models

class ProductReviewQuerySet(models.QuerySet[Any]):
    use_for_related_fields: bool
    def approved(self) -> ProductReviewQuerySet: ...
