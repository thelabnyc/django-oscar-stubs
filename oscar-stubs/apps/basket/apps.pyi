from typing import Any

from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class BasketConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    namespace: str

    summary_view: Any
    saved_view: Any
    add_view: Any
    add_voucher_view: Any
    remove_voucher_view: Any

    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
