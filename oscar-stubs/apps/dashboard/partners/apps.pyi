from typing import Any

from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from django.views import View
from oscar.core.application import OscarDashboardConfig

class PartnersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    list_view: type[View]
    create_view: type[View]
    manage_view: type[View]
    delete_view: type[View]
    user_link_view: type[View]
    user_unlink_view: type[View]
    user_create_view: type[View]
    user_select_view: type[View]
    user_update_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
