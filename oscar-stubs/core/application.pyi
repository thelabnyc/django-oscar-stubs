from collections.abc import Sequence
from typing import Any

from django.apps import AppConfig
from django.urls import URLPattern, URLResolver

class OscarConfigMixin:
    namespace: str | None
    login_url: str | None
    hidable_feature_name: str | None
    permissions_map: dict[str, Any]
    default_permissions: list[str] | None
    def __init__(self, app_name: str, app_module: Any, namespace: str | None = ..., **kwargs: Any) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
    def post_process_urls(self, urlpatterns: Sequence[URLPattern | URLResolver]) -> list[URLPattern | URLResolver]: ...
    def get_permissions(self, url: str | None) -> list[str] | None: ...
    def get_url_decorator(self, pattern: URLPattern) -> Any: ...
    @property
    def urls(self) -> tuple[list[URLPattern | URLResolver], str, str | None]: ...

class OscarConfig(OscarConfigMixin, AppConfig): ...

class OscarDashboardConfig(OscarConfig):
    login_url: str
