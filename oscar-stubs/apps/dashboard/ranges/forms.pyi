from typing import Any

from django import forms
from django.db.models import QuerySet

class RangeForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class RangeProductForm(forms.Form):
    query: forms.CharField
    file_upload: forms.FileField
    upload_type: forms.CharField
    product_range: Any
    products: QuerySet[Any]
    missing_skus: set[str]
    duplicate_skus: set[str]

    def __init__(self, product_range: Any, *args: Any, **kwargs: Any) -> None: ...
    def clean_query_with_upload_type(self, raw: str, upload_type: str) -> None: ...
    def get_products(self) -> QuerySet[Any] | list[Any]: ...
    def get_missing_skus(self) -> set[str]: ...
    def get_duplicate_skus(self) -> set[str]: ...

class RangeExcludedProductForm(RangeProductForm):
    def clean_query(self) -> str: ...
