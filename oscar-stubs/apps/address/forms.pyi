from typing import Any

from django import forms
from oscar.forms.mixins import PhoneNumberMixin

class AbstractAddressForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class UserAddressForm(PhoneNumberMixin, AbstractAddressForm):
    class Meta:
        model: Any
        fields: list[str]

    def __init__(self, user: Any, *args: Any, **kwargs: Any) -> None: ...
