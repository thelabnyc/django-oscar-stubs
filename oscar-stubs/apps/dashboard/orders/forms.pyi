from typing import Any

from django import forms
from oscar.apps.order.abstract_models import AbstractOrder

Order: type[AbstractOrder]

class OrderStatsForm(forms.Form):
    date_from: forms.DateField
    date_to: forms.DateField
    def get_filters(self) -> dict[str, Any]: ...
    def get_filter_description(self) -> str: ...

class OrderSearchForm(forms.Form):
    order_number: forms.CharField
    name: forms.CharField
    product_title: forms.CharField
    upc: forms.CharField
    partner_sku: forms.CharField
    status: forms.ChoiceField
    date_from: forms.DateField
    date_to: forms.DateField
    voucher: forms.CharField
    payment_method: forms.ChoiceField
    response_format: forms.ChoiceField

    format_choices: tuple[tuple[str, str], ...]
    status_choices: tuple[tuple[str, str], ...]

    def payment_method_choices(self) -> tuple[tuple[str, str], ...]: ...

class OrderNoteForm(forms.ModelForm):
    def __init__(self, order: Any, user: Any, *args: Any, **kwargs: Any) -> None: ...

    class Meta:
        model: type
        fields: list[str]

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class OrderStatusForm(forms.Form):
    new_status: forms.ChoiceField
    def __init__(self, order: Any, *args: Any, **kwargs: Any) -> None: ...
    @property
    def has_choices(self) -> bool: ...
