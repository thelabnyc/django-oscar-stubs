from typing import Any

from django.db.models import QuerySet
from oscar.apps.dashboard.catalogue.utils import partner_product_visibility_q as partner_product_visibility_q
from oscar.views.generic import (
    AbstractBulkAction,
    BulkAction,
    BulkEditMixin,
    IntermediateBulkAction,
    IntermediateBulkEditMixin,
)

MakePublicAction: type[BulkAction]
MakeNonPublicAction: type[BulkAction]
MakeProductsPublicAction: type[IntermediateBulkAction]
MakeProductsNonPublicAction: type[IntermediateBulkAction]
SetProductPriceAction: type[IntermediateBulkAction]

class PartnerProductFilterMixin:
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...

class ProductBulkActionMixin(IntermediateBulkEditMixin):
    def get_actions(self) -> dict[str, AbstractBulkAction | None]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class CategoryBulkActionMixin(BulkEditMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
