from typing import Any

from django import forms
from django.forms.widgets import FileInput

class ImageInput(FileInput):
    template_name: str
    def __init__(self, attrs: dict[str, Any] | None = ...) -> None: ...
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]: ...

class WYSIWYGTextArea(forms.Textarea):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

def datetime_format_to_js_date_format(datetime_format: str) -> str: ...
def datetime_format_to_js_time_format(datetime_format: str) -> str: ...
def datetime_format_to_js_datetime_format(datetime_format: str) -> str: ...
def datetime_format_to_js_input_mask(datetime_format: str) -> str: ...

class DateTimeWidgetMixin:
    template_name: str
    def get_format(self) -> str: ...
    def build_attrs(self, base_attrs: dict[str, Any], extra_attrs: dict[str, Any] | None = ...) -> dict[str, Any]: ...

class TimePickerInput(DateTimeWidgetMixin, forms.TimeInput):
    format_key: str
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]: ...

class DatePickerInput(DateTimeWidgetMixin, forms.DateInput):
    format_key: str
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]: ...

class DateTimePickerInput(DateTimeWidgetMixin, forms.DateTimeInput):
    format_key: str
    def __init__(self, *args: Any, include_seconds: bool = ..., **kwargs: Any) -> None: ...
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]: ...

class AdvancedSelect(forms.Select):
    disabled_values: set[str]
    def __init__(
        self,
        attrs: dict[str, Any] | None = ...,
        choices: Any = ...,
        disabled_values: tuple[Any, ...] = ...,
    ) -> None: ...
    def create_option(
        self,
        name: str,
        value: Any,
        label: str,
        selected: bool,
        index: int,
        subindex: int | None = ...,
        attrs: dict[str, Any] | None = ...,
    ) -> dict[str, Any]: ...

class RemoteSelect(forms.Select):
    lookup_url: str | None
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def build_attrs(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    def optgroups(self, name: str, value: list[str], attrs: dict[str, Any] | None = ...) -> list[Any]: ...

class MultipleRemoteSelect(RemoteSelect):
    allow_multiple_selected: bool

class NullBooleanSelect(forms.NullBooleanSelect):
    def __init__(self, attrs: dict[str, Any] | None = ...) -> None: ...
