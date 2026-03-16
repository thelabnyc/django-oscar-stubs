from typing import Any

from django.forms import fields

class ExtendedURLField(fields.URLField):
    default_validators: list[Any]
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def to_python(self, value: Any) -> str: ...
