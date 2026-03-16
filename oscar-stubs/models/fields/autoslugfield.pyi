from typing import Any

from django.db import models
from oscar.models.fields.slugfield import SlugField

class AutoSlugField(SlugField):
    separator: str
    overwrite: bool
    uppercase: bool
    allow_duplicates: bool
    def __init__(
        self,
        *args: Any,
        populate_from: str | list[str] | tuple[str, ...],
        separator: str = ...,
        overwrite: bool = ...,
        uppercase: bool = ...,
        allow_duplicates: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    def _slug_strip(self, value: str) -> str: ...
    def get_queryset(
        self, model_cls: type[models.Model], slug_field: models.Field[Any, Any]
    ) -> models.QuerySet[Any]: ...
    def slugify_func(self, content: str) -> str: ...
    def create_slug(self, model_instance: models.Model, add: bool) -> str: ...
    def pre_save(self, model_instance: models.Model, add: bool) -> str: ...
    def get_internal_type(self) -> str: ...
    def deconstruct(self) -> tuple[str, str, list[Any], dict[str, Any]]: ...
