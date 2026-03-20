from django.apps import AppConfig
from django.urls import URLPattern, URLResolver
from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class CatalogueOnlyConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    namespace: str
    detail_view: type
    catalogue_view: type
    category_view: type
    range_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...

class CatalogueReviewsOnlyConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
    reviews_app: AppConfig
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...

class CatalogueConfig(CatalogueOnlyConfig, CatalogueReviewsOnlyConfig): ...
