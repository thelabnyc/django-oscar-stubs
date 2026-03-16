from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarDashboardConfig

class OrdersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    order_list_view: type
    order_detail_view: type
    shipping_address_view: type
    line_detail_view: type
    order_stats_view: type

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
