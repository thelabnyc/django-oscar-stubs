from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class CustomerConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    namespace: str

    summary_view: Any
    order_history_view: Any
    order_detail_view: Any
    anon_order_detail_view: Any
    anon_order_form_view: Any
    order_line_view: Any
    address_list_view: Any
    address_create_view: Any
    address_update_view: Any
    address_delete_view: Any
    address_change_status_view: Any
    email_list_view: Any
    email_detail_view: Any
    login_view: Any
    logout_view: Any
    register_view: Any
    profile_view: Any
    profile_update_view: Any
    profile_delete_view: Any
    change_password_view: Any
    notification_inbox_view: Any
    notification_archive_view: Any
    notification_update_view: Any
    notification_detail_view: Any
    alert_list_view: Any
    alert_create_view: Any
    alert_confirm_view: Any
    alert_cancel_view: Any
    wishlists_add_product_view: Any
    wishlists_list_view: Any
    wishlists_detail_view: Any
    wishlists_create_view: Any
    wishlists_create_with_product_view: Any
    wishlists_update_view: Any
    wishlists_delete_view: Any
    wishlists_remove_product_view: Any
    wishlists_move_product_to_another_view: Any

    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
