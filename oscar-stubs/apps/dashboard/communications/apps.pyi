from typing import Any

from django.urls import URLPattern, URLResolver
from django.views import View
from oscar.core.application import OscarDashboardConfig

class CommunicationsDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    list_view: type[View]
    update_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
