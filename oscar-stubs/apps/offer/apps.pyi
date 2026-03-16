from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class OfferConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    namespace: str

    detail_view: Any
    list_view: Any

    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
