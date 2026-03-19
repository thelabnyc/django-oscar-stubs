from typing import Any

from django.urls import URLPattern, URLResolver
from django.views import View
from oscar.core.application import OscarDashboardConfig

class CatalogueDashboardConfig(OscarDashboardConfig):
    label: str
    name: str
    verbose_name: str
    default_permissions: list[str]
    permissions_map: dict[str, Any]

    product_list_view: type[View]
    product_lookup_view: type[View]
    product_create_redirect_view: type[View]
    product_createupdate_view: type[View]
    product_delete_view: type[View]
    product_class_create_view: type[View]
    product_class_update_view: type[View]
    product_class_list_view: type[View]
    product_class_delete_view: type[View]
    category_list_view: type[View]
    category_detail_list_view: type[View]
    category_create_view: type[View]
    category_update_view: type[View]
    category_delete_view: type[View]
    stock_alert_view: type[View]
    attribute_option_group_create_view: type[View]
    attribute_option_group_list_view: type[View]
    attribute_option_group_update_view: type[View]
    attribute_option_group_delete_view: type[View]
    option_list_view: type[View]
    option_create_view: type[View]
    option_update_view: type[View]
    option_delete_view: type[View]

    def configure_permissions(self) -> None: ...
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
