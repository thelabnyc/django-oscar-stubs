from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from oscar.views.generic import BulkEditMixin

class PartnerProductFilterMixin:
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...

class PublicVisibilityUpdateMixin(BulkEditMixin):
    actions: tuple[str, ...]
    def make_non_public(self, request: HttpRequest, records: Any) -> HttpResponse: ...
    def make_public(self, request: HttpRequest, records: Any) -> HttpResponse: ...
