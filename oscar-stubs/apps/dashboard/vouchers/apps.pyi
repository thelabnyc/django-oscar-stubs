from typing import Any

from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from django.views import View
from oscar.core.application import OscarDashboardConfig

class VouchersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    list_view: type[View]
    create_view: type[View]
    update_view: type[View]
    delete_view: type[View]
    stats_view: type[View]
    set_list_view: type[View]
    set_create_view: type[View]
    set_update_view: type[View]
    set_detail_view: type[View]
    set_download_view: type[View]
    set_delete_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
