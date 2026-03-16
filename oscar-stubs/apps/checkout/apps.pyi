from typing import Any

from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class CheckoutConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    namespace: str
    index_view: type
    shipping_address_view: type
    user_address_update_view: type
    user_address_delete_view: type
    shipping_method_view: type
    payment_method_view: type
    payment_details_view: type
    thankyou_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
    def get_url_decorator(self, pattern: URLPattern) -> Any | None: ...
