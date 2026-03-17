from typing import Any

from django.db.models import QuerySet

class PartnerProductFilterMixin:
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
