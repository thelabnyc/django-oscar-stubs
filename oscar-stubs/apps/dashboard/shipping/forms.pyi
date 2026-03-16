from typing import Any

from django import forms

class WeightBasedForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class WeightBandForm(forms.ModelForm):
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...

    class Meta:
        model: type
        fields: tuple[str, ...]
