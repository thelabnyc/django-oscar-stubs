from typing import Any

from django import forms

class VoucherForm(forms.ModelForm):
    offers: forms.ModelMultipleChoiceField
    def clean_code(self) -> str: ...

    class Meta:
        model: type
        fields: list[str]
        widgets: dict[str, forms.Widget]

class VoucherSearchForm(forms.Form):
    name: forms.CharField
    code: forms.CharField
    offer_name: forms.CharField
    is_active: forms.NullBooleanField
    in_set: forms.NullBooleanField
    has_offers: forms.NullBooleanField
    basic_fields: list[str]
    def clean_code(self) -> str: ...

class VoucherSetForm(forms.ModelForm):
    usage: forms.ChoiceField
    offers: forms.ModelMultipleChoiceField
    def clean_count(self) -> int: ...
    def save(self, commit: bool = ...) -> Any: ...

    class Meta:
        model: type
        fields: list[str]
        widgets: dict[str, forms.Widget]

class VoucherSetSearchForm(forms.Form):
    code: forms.CharField
    def clean_code(self) -> str: ...
