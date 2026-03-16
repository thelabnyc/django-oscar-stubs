from typing import Any

from django import forms

def get_offer_type_choices() -> tuple[tuple[str, str], ...]: ...

class MetaDataForm(forms.ModelForm):
    offer_type: forms.ChoiceField
    def clean_offer_type(self) -> str: ...

    class Meta:
        model: type
        fields: tuple[str, ...]

class RestrictionsForm(forms.ModelForm):
    start_datetime: forms.DateTimeField
    end_datetime: forms.DateTimeField

    class Meta:
        model: type
        fields: tuple[str, ...]

    def save(self, *args: Any, **kwargs: Any) -> Any: ...

class ConditionForm(forms.ModelForm):
    custom_condition: forms.ChoiceField

    class Meta:
        model: type
        fields: list[str]

    def save(self, *args: Any, **kwargs: Any) -> Any: ...

class BenefitForm(forms.ModelForm):
    custom_benefit: forms.ChoiceField

    class Meta:
        model: type
        fields: list[str]

    def save(self, *args: Any, **kwargs: Any) -> Any: ...

class OfferSearchForm(forms.Form):
    name: forms.CharField
    is_active: forms.NullBooleanField
    offer_type: forms.ChoiceField
    has_vouchers: forms.NullBooleanField
    voucher_code: forms.CharField
    basic_fields: list[str]
    @property
    def is_voucher_offer_type(self) -> bool: ...
