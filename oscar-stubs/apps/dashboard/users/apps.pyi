from typing import Any

from django.urls import URLPattern, URLResolver
from django.views import View
from oscar.core.application import OscarDashboardConfig

class UsersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    index_view: type[View]
    user_detail_view: type[View]
    password_reset_view: type[View]
    alert_list_view: type[View]
    alert_update_view: type[View]
    alert_delete_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
