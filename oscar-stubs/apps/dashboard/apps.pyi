from django.apps import AppConfig
from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarDashboardConfig

class DashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    namespace: str
    permissions_map: dict[str, tuple[list[str], ...]]

    index_view: type
    login_view: type
    catalogue_app: AppConfig
    reports_app: AppConfig
    orders_app: AppConfig
    users_app: AppConfig
    pages_app: AppConfig
    partners_app: AppConfig
    offers_app: AppConfig
    ranges_app: AppConfig
    reviews_app: AppConfig
    vouchers_app: AppConfig
    comms_app: AppConfig
    shipping_app: AppConfig

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
