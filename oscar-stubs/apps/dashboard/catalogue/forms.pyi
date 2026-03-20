from collections.abc import Callable
from typing import Any

from django import forms

class SEOFormMixin:
    seo_fields: list[str]
    def primary_form_fields(self) -> list[Any]: ...
    def seo_form_fields(self) -> list[Any]: ...
    def is_seo_field(self, field: Any) -> bool: ...

class CategoryForm(SEOFormMixin, forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class ProductClassSelectForm(forms.Form):
    product_class: forms.ModelChoiceField

class ProductSearchForm(forms.Form):
    upc: forms.CharField
    title: forms.CharField

class StockRecordForm(forms.ModelForm):
    user: Any
    def __init__(self, product_class: Any, user: Any, *args: Any, **kwargs: Any) -> None: ...

    class Meta:
        model: type
        fields: list[str]

class ProductForm(SEOFormMixin, forms.ModelForm):
    FIELD_FACTORIES: dict[str, Callable[..., forms.Field | None]]

    class Meta:
        model: type
        fields: list[str]
        widgets: dict[str, forms.Widget]

    def __init__(self, product_class: Any, *args: Any, data: Any = ..., parent: Any = ..., **kwargs: Any) -> None: ...
    def set_initial(self, product_class: Any, parent: Any, kwargs: dict[str, Any]) -> None: ...
    def set_initial_attribute_values(self, product_class: Any, kwargs: dict[str, Any]) -> None: ...
    def add_attribute_fields(self, product_class: Any, is_parent: bool = ...) -> None: ...
    def get_attribute_field(self, attribute: Any) -> forms.Field | None: ...
    def delete_non_child_fields(self) -> None: ...
    def _post_clean(self) -> None: ...

class StockAlertSearchForm(forms.Form):
    status: forms.CharField

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model: type
        fields: tuple[str, ...]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]
        widgets: dict[str, forms.Widget]

    def __init__(self, *args: Any, data: Any = ..., **kwargs: Any) -> None: ...
    def get_display_order(self) -> int: ...

class ProductRecommendationForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]
        widgets: dict[str, forms.Widget]

class ProductClassForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class ProductAttributesForm(forms.ModelForm):
    def clean_code(self) -> str: ...

    class Meta:
        model: type
        fields: list[str]

class AttributeOptionGroupForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class AttributeOptionForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class OptionForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]
