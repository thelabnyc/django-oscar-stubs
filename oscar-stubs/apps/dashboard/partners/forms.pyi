from typing import Any

from django import forms

ROLE_CHOICES: tuple[tuple[str, str], ...]

class PartnerSearchForm(forms.Form):
    name: forms.CharField

class PartnerCreateForm(forms.ModelForm):
    class Meta:
        model: type
        fields: tuple[str, ...]

class NewUserForm(forms.ModelForm):
    role: forms.ChoiceField
    partner: Any
    def __init__(self, partner: Any, *args: Any, **kwargs: Any) -> None: ...
    def save(self) -> Any: ...

    class Meta:
        model: type
        fields: list[str]

class ExistingUserForm(forms.ModelForm):
    role: forms.ChoiceField
    password1: forms.CharField
    password2: forms.CharField
    def clean_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> Any: ...

    class Meta:
        model: type
        fields: list[str]

class UserEmailForm(forms.Form):
    email: forms.CharField

class PartnerAddressForm(forms.ModelForm):
    name: forms.CharField

    class Meta:
        fields: tuple[str, ...]
        model: type
