from typing import Any

from django import forms
from django.db.models import QuerySet
from django.http import HttpRequest
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.dashboard.catalogue.utils import partner_product_visibility_q as partner_product_visibility_q
from oscar.apps.partner.abstract_models import AbstractStockRecord
from oscar.views.generic import BulkAction, IntermediateBulkAction

ProductBulkActionForm: type[forms.Form]
SetProductPriceForm: type[forms.Form]
Product: type[AbstractProduct]
StockRecord: type[AbstractStockRecord]

class BaseSetPublicStatusAction(BulkAction):
    is_public: bool
    def execute(self, request: HttpRequest, objects: QuerySet[Any]) -> None: ...

class MakePublicAction(BaseSetPublicStatusAction): ...
class MakeNonPublicAction(BaseSetPublicStatusAction): ...

class ProductIntermediateAction(IntermediateBulkAction):
    supported_structures: list[str] | None
    def filter_products_queryset(self, qs: QuerySet[Any]) -> QuerySet[Any]: ...
    def execute(self, request: HttpRequest, objects: QuerySet[Any], form: Any) -> None: ...

class BaseSetProductsPublicStatusAction(ProductIntermediateAction):
    is_public: bool
    def execute(self, request: HttpRequest, objects: QuerySet[Any], form: Any) -> None: ...

class MakeProductsPublicAction(BaseSetProductsPublicStatusAction): ...
class MakeProductsNonPublicAction(BaseSetProductsPublicStatusAction): ...

class SetProductPriceAction(ProductIntermediateAction):
    def filter_products_queryset(self, qs: QuerySet[Any]) -> QuerySet[Any]: ...
    def execute(self, request: HttpRequest, objects: QuerySet[Any], form: Any) -> None: ...
