from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarDashboardConfig

class CatalogueDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    product_list_view: type
    product_lookup_view: type
    product_create_redirect_view: type
    product_createupdate_view: type
    product_delete_view: type
    product_class_create_view: type
    product_class_update_view: type
    product_class_list_view: type
    product_class_delete_view: type
    category_list_view: type
    category_detail_list_view: type
    category_create_view: type
    category_update_view: type
    category_delete_view: type
    stock_alert_view: type
    attribute_option_group_create_view: type
    attribute_option_group_list_view: type
    attribute_option_group_update_view: type
    attribute_option_group_delete_view: type
    option_list_view: type
    option_create_view: type
    option_update_view: type
    option_delete_view: type

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
