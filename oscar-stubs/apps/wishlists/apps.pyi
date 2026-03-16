from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class WishlistsConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    namespace: str
    wishlist_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
