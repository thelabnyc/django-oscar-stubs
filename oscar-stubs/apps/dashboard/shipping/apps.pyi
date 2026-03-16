from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarDashboardConfig

class ShippingDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    weight_method_list_view: type
    weight_method_create_view: type
    weight_method_edit_view: type
    weight_method_delete_view: type
    weight_method_detail_view: type
    weight_band_edit_view: type
    weight_band_delete_view: type

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
