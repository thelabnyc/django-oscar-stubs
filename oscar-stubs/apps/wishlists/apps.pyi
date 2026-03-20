from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class WishlistsConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    namespace: str
    wishlist_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
