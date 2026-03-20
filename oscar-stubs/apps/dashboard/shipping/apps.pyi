from typing import Any

from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from django.views import View
from oscar.core.application import OscarDashboardConfig

class ShippingDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    weight_method_list_view: type[View]
    weight_method_create_view: type[View]
    weight_method_edit_view: type[View]
    weight_method_delete_view: type[View]
    weight_method_detail_view: type[View]
    weight_band_edit_view: type[View]
    weight_band_delete_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
