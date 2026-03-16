from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarDashboardConfig

class VouchersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    list_view: type
    create_view: type
    update_view: type
    delete_view: type
    stats_view: type
    set_list_view: type
    set_create_view: type
    set_update_view: type
    set_detail_view: type
    set_download_view: type
    set_delete_view: type

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
