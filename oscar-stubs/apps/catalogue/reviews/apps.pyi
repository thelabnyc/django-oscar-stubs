from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class CatalogueReviewsConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    hidable_feature_name: str
    detail_view: type
    create_view: type
    vote_view: type
    list_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
