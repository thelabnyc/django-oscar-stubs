from typing import Any

from django.urls import URLPattern, URLResolver
from django.views import View
from oscar.core.application import OscarDashboardConfig

class OffersDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    list_view: type[View]
    metadata_view: type[View]
    condition_view: type[View]
    benefit_view: type[View]
    restrictions_view: type[View]
    delete_view: type[View]
    detail_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
