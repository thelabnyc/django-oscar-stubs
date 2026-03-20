from typing import Any

from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from django.views import View
from oscar.core.application import OscarDashboardConfig

class OrdersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    order_list_view: type[View]
    order_detail_view: type[View]
    shipping_address_view: type[View]
    line_detail_view: type[View]
    order_stats_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
